from functions import *
import time

handle, window, PId = get_fortnite_window()
img = screenshot_resize(window, handle, "./screenshot.png")
stage = None
# function to check stage goes here


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
        self.access_level = tier
        self.print_area = listBoxLogger
        self.jumpSecs = jumpSecs
        self.statsSSBool = statsSSBool
        self.pbBool = pbBool
        self.pbAccTkn = pbAccTkn
        self.landInTreeBool = landInTreeBool
        self.handle, self.window, self.PId = get_fortnite_window()
        self.img = screenshot_resize(self.window, self.handle, "./screenshot.png")
        self.stage = None
        self.player_mover = PlayerMovement("./icons/player_cursor.png")
        self.crouched = False
        self.numberGames = 0
        self.takeScreenshot = True

    def send_image_pushbullet(self, access_token, img_path, game_num):
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
            "body": "FortBot screenshot from game %d" % game_num,
            "file_name": file_name,
            "file_type": file_type,
            "file_url": file_url,
        }
        res = requests.post(url, json=data, headers=headers)
        if res.status_code != 200:
            self.print_to_GUI("Error pushing to phone", "error")
        self.print_to_GUI("Pushed screenshot to phone")

    def startLoop(self) -> None:
        while True:
            # determine stage here using fictional function self.stage=determineStage()
            if self.stage == "solo-lobby":
                img = screenshot_resize(window, handle, "./screenshot.png")
                clickbtn(
                    "./icons/play_button.png",
                    img,
                )

            if self.stage == "party-lobby":
                img = screenshot_resize(window, handle, "./screenshot.png")
                clickbtn(
                    "./icons/ready_button.png",
                    img,
                )

            if self.stage == "pre-jump":
                self.numberGames += 1
                img = screenshot_resize(window, handle, "./screenshot.png")
                if findbtn("./icons/bus_icon_square.png", img):
                    time.sleep(self.jumpSecs)
                    pyautogui.press("space")
                    if self.landInTreeBool:
                        print("goin to the treeeees")
                        pyautogui.press("space")
                        pyautogui.press("m")
                        time.sleep(2.0)
                        self.player_mover.land_at_closest_loc()
                        print("lovely trees you got there")
                        self.waitToCrouchTS = datetime.datetime.now().timestamp()
                        self.stage = "in-game"
                else:
                    # self.stage = determineStage()
                    continue

            if self.stage == "in-game":
                if self.crouched == False:
                    if datetime.datetime.now().timestamp() - self.waitToCrouchTS > 80.0:
                        pyautogui.press("ctrl")
                        self.crouched = True
                        print("When will this ennnnddd")

            if self.stage == "post-game":
                if self.pbBool and self.takeScreenshot:
                    stats = "./tempScreenshot.png"
                    pyautogui.screenshot(stats)
                    self.takeScreenshot = False
                    self.send_image_pushbullet(self.pbAccTkn, stats, self.numberGames)

            if self.stage == "return-lobby":

