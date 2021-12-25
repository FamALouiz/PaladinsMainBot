from utilityfuncs import *
from tkinter import *
import time, requests, datetime, random, plrmovement
from icons import *
import threading


class mainLoop:
    """
    Houses all bot functionalities and states
    """

    def __init__(
        self,
        listBoxLogger,
        jumpSecs,
        statsSSBool,
        pbBool,
        pbAccTkn,
        landInTreeBool,
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
        self.jumpTime = random.choice(range(jumpSecs[0], jumpSecs[1]))
        self.statsSSBool = statsSSBool
        self.pbBool = pbBool
        self.pbAccTkn = pbAccTkn
        self.landInTreeBool = landInTreeBool
        self.invalid = False
        self.inbus = False
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
        self.isrunning = False
        self.stop_event = threading.Event()

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
        if self.isrunning:
            self.isrunning = False
            self.stop_event.set()
            self.loopThread = None
            self.print_to_GUI("Bot stopping...")
            print("bot stopped???")

    def startLoop(self) -> bool:
        """
        Main loop of the bot which goes through the stages and does its necessary action
        """
        if not self.isrunning:
            self.stop_event.clear()
            self.isrunning = True
            self.loopThread = threading.Thread(target=self.actual_loop)
            self.loopThread.start()
            return True
        return False

    def runningchck(self):
        return self.isrunning

    def actual_loop(self):
        isfortnite()
        self.stage = check_stage(self.buttons, lambda: self.runningchck())
        prevstage = ""
        stagecount = 0
        ingamecount = 0
        while self.isrunning:
            print(self.stage)
            if not self.isrunning:
                break
            if self.stage == "lobby":
                self.print_to_GUI("Looking for play button")
                if check_btns(stage_btns[self.stage], lambda: self.runningchck()):
                    btnlist["play_button"].click()
                    self.print_to_GUI("Play button clicked (waiting for game to start)")
                    time.sleep(30)
                    self.stage = "in-jump"

            elif self.stage == "in-bus":
                if check_btns(stage_btns[self.stage], lambda: self.runningchck()):
                    self.print_to_GUI("Waiting to jump out of the bus")
                    self.numberGames += 1
                    if self.access_level > 0:
                        pyautogui.press("b")
                        self.print_to_GUI("Thanking the bus driver :)")
                    time.sleep(1)
                    self.stage = "in-jump"

            elif self.stage == "in-jump":
                if check_btns(stage_btns[self.stage], lambda: self.runningchck()):
                    self.print_to_GUI(f"Jumping out after {self.jumpTime} seconds")
                    time.sleep(self.jumpTime)
                    pyautogui.press("space")
                    time.sleep(2)
                    pyautogui.press("space")
                    self.print_to_GUI("Jumped out")
                    if self.landInTreeBool:
                        if pyautogui.size() == (1920, 1080):
                            self.print_to_GUI("Navigating towards the nearest tree")
                            pyautogui.press("space")
                            self.player_mover.land_at_closest_loc()
                            self.print_to_GUI("Tree reached")
                            self.waitToCrouchTS = datetime.datetime.now().timestamp()
                        else:
                            self.print_to_GUI("Screen is not 1920x1080 cannot land on trees")
                    else:
                        time.sleep(60)
                    self.stage = "in-game"
                else:
                    time.sleep(1)

            elif self.stage == "in-game":
                if check_btns(stage_btns[self.stage], lambda: self.runningchck()):
                    if not self.crouched:
                        if datetime.datetime.now().timestamp() - self.waitToCrouchTS > 80.0:
                            pyautogui.press("ctrl")
                            self.crouched = True
                            self.print_to_GUI("Waiting to die")
                    self.antiAFK()
                    time.sleep(10)
                    self.stage = "post-game"
                    if prevstage == "in-game":
                        ingamecount += 1
                    if ingamecount > 80:
                        self.print_to_GUI("maybe??? in loop")
                        self.stage = check_stage(self.buttons, lambda: self.runningchck())
                        ingamecount = 0

            elif self.stage == "post-game":
                if check_btns(stage_btns[self.stage], lambda: self.runningchck()):
                    if self.pbBool and self.takeScreenshot:
                        stats = f"./screenshots/screenshot_{self.numberGames}.png"
                        pyautogui.screenshot(stats)
                        self.takeScreenshot = False
                        self.send_image_pushbullet(self.pbAccTkn, stats)
                    self.stage = "claim-rewards"
                else:
                    self.print_to_GUI("Waiting to die")
                    time.sleep(1)
                    self.stage = "in-game"

            elif self.stage == "claim-rewards":
                btns = check_btns(stage_btns[self.stage], lambda: self.runningchck())
                if btns:
                    self.print_to_GUI("Claiming rewards")
                    for btnnn in btns:
                        if btnlist[btnnn].cords is not None:
                            btnlist[btnnn].click()
                    self.stage = "lobby"

            if self.stage == prevstage:
                stagecount += 1
            else:
                prevstage = self.stage
                stagecount = 0
            if stagecount > 15:
                self.print_to_GUI("Stuck in loop")
                time.sleep(1)
                self.stage = check_stage(self.buttons, lambda: self.runningchck())
                stagecount = 0
