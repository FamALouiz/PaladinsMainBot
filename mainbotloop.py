from functions import *
from tkinter import *
import time, requests, datetime, random, plrmovement
from icons import *


class mainLoop:
    """
    Houses all bot functionalities and states
    """

    def __init__(
        self,
        listBoxLogger: object,
        jumpSecs: int,
        statsSSBool: bool,
        pbBool: bool,
        pbAccTkn: str,
        landInTreeBool: bool,
        tier=0,
    ) -> None:
        """
        listBoxLogger = Text box in GUI
        jumpSecs = Number of secs before jumping from bus
        pbBool = Whether or not Push Bullet (PB) will be used to save stats screenshots
        pbAccTkn =  PB account token to upload screenshot to
        landInTreeBool = whether the user wants to land in tree
        tier = user access level
        """
        self.lastMessage = None
        self.access_level = tier
        self.print_area = listBoxLogger
        self.jumpSecs = jumpSecs
        self.statsSSBool = statsSSBool
        self.pbBool = pbBool
        self.pbAccTkn = pbAccTkn
        self.landInTreeBool = landInTreeBool
        self.invalid = False
        try:
            get_fortnite_window()
        except:
            self.print_to_GUI("Fortnite is not running, please launch the game")
            self.invalid = True
            return
        self.img = screenshot_resize("./screenshot.png")
        self.stage = None
        self.player_mover = plrmovement.Player("./icons/player_cursor.png")
        self.crouched = False
        self.numberGames = 0
        self.takeScreenshot = True
        self.buttons = btnlist

    def print_to_GUI(self, msg, type="basic"):
        if msg == self.lastMessage:
            return
        else:
            self.print_area.configure(state="normal")
            autoscroll = False
            ts = datetime.datetime.fromtimestamp(time.time()).strftime("%Y/%m/%d %H:%M:%S || ")
            if self.print_area.yview()[1] == 1:
                autoscroll = True
            self.print_area.insert(END, ts + msg + "\n", type)
            self.lastMessage = msg
            if autoscroll:
                self.print_area.see(END)
        self.print_area.configure(state="disabled")

    def send_image_pushbullet(self, access_token, img_path):
        url = "https://api.pushbullet.com/v2/upload-request"
        headers = {"Access-Token": access_token, "Content-Type": "application/json"}
        data = {"file_name": img_path, "file_type": "image/jpeg"}
        res = requests.post(url, json=data, headers=headers)
        if res.status_code != 200:
            self.print_to_GUI("Error authenticating with Access Token", "error")
            return
        resJson = res.json()
        file_name = resJson["file_name"]
        file_type = resJson["file_type"]
        file_url = resJson["file_url"]
        upload_url = resJson["upload_url"]
        data = resJson["data"]
        data["file"] = open(img_path, "rb")
        headers = {"Access-Token": access_token}
        res = requests.post(upload_url, files=data, headers=headers)
        if res.status_code != 204:
            self.print_to_GUI("Error uploading file", "error")
            return
        url = "https://api.pushbullet.com/v2/pushes"
        headers = {"Access-Token": access_token, "Content-Type": "application/json"}
        data = {
            "type": "file",
            "body": f"FortBot screenshot from game {self.numberGames}",
            "file_name": file_name,
            "file_type": file_type,
            "file_url": file_url,
        }
        res = requests.post(url, json=data, headers=headers)
        if res.status_code != 200:
            self.print_to_GUI("Error pushing to phone", "error")
        if res.status_code == 200:
            self.print_to_GUI("Pushed screenshot to phone")

    def antiAFK(self):
        time.sleep(random.randrange(0, 10))
        pyautogui.click()
        pyautogui.press("w")
        pyautogui.press("space")
        pyautogui.press("d")
        pyautogui.press("a")
        pyautogui.press("s")
        pyautogui.press("ctrl")

    def stopLoop(self):
        self.stage = "exit"
        self.print_to_GUI("Bot stopping...")

    def startLoop(self) -> None:
        """
        Main loop of the bot which goes through the stages and does its necessary action
        """
        while True:
            self.stage = check_stage(self.buttons)
            if self.stage == "solo-lobby":
                self.print_to_GUI("Looking for play button")
                img = screenshot_resize("./screenshot.png")
                clickbtn(
                    "./icons/play_button.png",
                    img,
                )
                self.print_to_GUI("Play button clicked (waiting for game to start)")

            elif self.stage == "party-lobby":
                self.print_to_GUI("Looking for ready button")
                img = screenshot_resize("./screenshot.png")
                clickbtn(
                    "./icons/ready_button.png",
                    img,
                )
                self.print_to_GUI("Ready button clicked (waiting for game to start)")

            elif self.stage == "in-bus":
                self.print_to_GUI("Waiting to jump out of the bus")
                self.numberGames += 1
                if self.access_level > 0:
                    pyautogui.press("b")
                    self.print_to_GUI("Thanking the bus driver :)")

            elif self.stage == "in-jump":
                self.print_to_GUI(f"Jumping out after {self.jumpSecs} seconds")
                time.sleep(self.jumpSecs)
                pyautogui.press("space")
                self.print_to_GUI("Jumped out")
                if self.landInTreeBool:
                    self.print_to_GUI("Navigating towards the nearest tree")
                    pyautogui.press("space")
                    pyautogui.press("m")
                    time.sleep(2.0)
                    self.player_mover.land_at_closest_loc()
                    self.print_to_GUI("Tree reached")
                    self.waitToCrouchTS = datetime.datetime.now().timestamp()

            elif self.stage == "in-game":
                if self.crouched == False:
                    if datetime.datetime.now().timestamp() - self.waitToCrouchTS > 80.0:
                        pyautogui.press("ctrl")
                        self.crouched = True
                        self.print_to_GUI("Waiting to die")
                self.antiAFK()

            elif self.stage == "post-game":
                if self.pbBool and self.takeScreenshot:
                    stats = "./tempScreenshot.jpeg"
                    pyautogui.screenshot(stats)
                    self.takeScreenshot = False
                    self.send_image_pushbullet(self.pbAccTkn, stats)
                else:
                    self.stage = "claim-rewards"

            elif self.stage == "claim-rewards":
                img = screenshot_resize("./screenshot.png")
                if findbtn("./icons/collect_button.png", img):
                    clickbtn("./icons/collect_button.png", img)
                else:
                    self.stage = "claim-rewards-next"

            elif self.stage == "claim-rewards-next":
                img = screenshot_resize("./screenshot.png")
                if findbtn("./icons/collect_button_next.png", img):
                    clickbtn("./icons/collect_button_next.png", img)
                else:
                    self.stage = check_stage(self.buttons)

            elif self.stage == "continue":
                img = screenshot_resize("./screenshot.png")
                if findbtn("./icons/collect_button_next.png", img):
                    clickbtn("./icons/collect_button_next.png", img)
                elif findbtn("./icons/return_button.png", img):
                    clickbtn("./icons/return_button.png", img)
                else:
                    self.stage = "solo-lobby"

            elif self.stage == "exit":
                self.print_to_GUI("Bot closed")
                return
            else:
                self.stage = check_stage(self.buttons)
