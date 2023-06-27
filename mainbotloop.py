from utilityfuncs import *
from tkinter import *
import time, requests, datetime
from icons import *
import threading
import os

orb = cv2.ORB_create()

champion = "GROVER"
antiAFK = None
championType = "Support"
championSelected = False
championPath = eval(f"r'PaladinMainbot_pngs\{championType}\{champion}'")
championIcon = eval(f"r'PaladinMainbot_pngs\{championType}\{champion}\\0ChampIcon.png'")

iconNames = ["Lobby Play", "Join Queue", "Error", "Champion lockin"]
championIconNames = ["Talent", "Loadout", "Equip"]

iconlist = [
    os.path.join(championPath, f)
    for f in os.listdir(championPath)
    if f.endswith(".png")
][1:]


icons = ["Talent", "Loadout", "Equip"][1:]

iconsStart = [
    r"PaladinMainbot_pngs\1LobbyPlay.png",
    r"PaladinMainbot_pngs\2JoinQueue.png",
    r"PaladinMainbot_pngs\3Error.png",
    r"PaladinMainbot_pngs\5Champlockin.png",
]

iconsRedo = iconsStart[3]

iconRequeue = r"PaladinMainbot_pngs\ReQueue.png"

champion = None
championType = None


class PositionableSequenceIterator:
    def __init__(self, sequence):
        self.seq = sequence
        self._nextpos = 0

    @property
    def pos(self):
        pos = self._nextpos
        return 0 if pos is None else pos - 1

    @pos.setter
    def pos(self, newpos):
        if not 0 <= newpos < len(self.seq):
            raise IndexError(newpos)
        self._nextpos = newpos

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.seq[self._nextpos or 0]
        except IndexError:
            raise StopIteration
        finally:
            self._nextpos += 1


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
        times,
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
        self.inbus = False
        self.waitToCrouchTS = 0
        self.firstInGame = True
        self.tier = tier
        self.times = 0
        self.count = 1
        self.championPath = None
        self.championIcon = None
        self.iconlist = None
        self.icons = None
        self.resizeX = 1
        self.resizeY = 1
        self.current = None
        """
        try:
            get_fortnite_window()
        except:
            self.print_to_GUI(
                "Paladins is not running, please launch the game", "error"
            )
            self.invalid = True
            return
        """
        # self.img = screenshot_resize("./screenshot.png")
        self.stage = None
        # self.player_mover = plrmovement.Player("./icons/player_cursor.png")
        self.crouched = False
        self.numberGames = 0
        self.takeScreenshot = False
        # self.buttons = btnlist
        self.isrunning = False
        self.stop_event = threading.Event()

    def print_to_GUI(self, msg, type="basic"):
        if msg == self.lastMessage:
            return
        else:
            self.print_area.configure(state="normal")
            autoscroll = False
            ts = datetime.datetime.fromtimestamp(time.time()).strftime(
                "%Y/%m/%d %H:%M:%S || "
            )
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
            "body": f"Paladinsbot screenshot from game {self.count}",
            "file_name": file_name,
            "file_type": file_type,
            "file_url": file_url,
        }
        res = requests.post(url, json=data, headers=headers)
        if res.status_code != 200:
            self.print_to_GUI("Error pushing to phone", "error")
        if res.status_code == 200:
            self.print_to_GUI("Pushed screenshot to phone")

    def updateData(self):
        self.championPath = eval(f"r'PaladinMainbot_pngs\{championType}\{champion}'")
        self.championIcon = eval(
            f"r'PaladinMainbot_pngs\{championType}\{champion}\\0ChampIcon.png'"
        )

        self.iconlist = [
            os.path.join(self.championPath, f)
            for f in os.listdir(self.championPath)
            if f.endswith(".png")
        ][1:]

    def pickChampion(self):
        time.sleep(2)
        if not self.isrunning:
            return
        iterator = PositionableSequenceIterator(
            [[a, b] for a, b in zip(self.iconlist, championIconNames)]
        )
        flag = True
        if not self.isrunning:
            return
        for i in iterator:
            if not self.isrunning:
                return
            icon = i[0]
            name = i[1]
            try:
                s_width, s_height = pyautogui.size()
                siz_x, siz_y = Image.open(icon).size
                image = Image.open(icon).resize(
                    (int(siz_x * (s_width / 1920)), int(siz_y * (s_height / 1080))),
                    Image.ANTIALIAS,
                )
                pyautogui.click(
                    pyautogui.center(
                        pyautogui.locateOnScreen(
                            image,
                            confidence=0.75,
                        )
                    )
                )
                pyautogui.doubleClick()
                self.print_to_GUI(f"{name} chosen" if name != "Equip" else "Equiped")
            except:
                if flag:
                    self.print_to_GUI(f"Didn't find {name} button ... waiting for it")
                    flag = False
                iterator.pos = iterator.pos if iterator.pos > 0 else 0
            time.sleep(0.3)

        time.sleep(5)

    def firstGame(self):
        self.startGame()
        self.pickChampion()
        self.inGameAndRequeue()
        if self.isrunning:
            self.print_to_GUI(f"Game #{self.count}", "control")
        elif not self.isrunning:
            return
        if self.pbBool and self.statsSSBool and self.isrunning:
            stats = f"./screenshots/screenshot_{self.count}.png"
            pyautogui.screenshot(stats)
            self.send_image_pushbullet(self.pbAccTkn, stats)

        elif self.statsSSBool and self.isrunning:
            stats = f"./screenshots/screenshot_{self.count}.png"
            pyautogui.screenshot(stats)

        elif self.pbBool and self.isrunning:
            stats = f"./pushbullet/screenshot_{self.count}.png"
            pyautogui.screenshot(stats)
            self.send_image_pushbullet(self.pbAccTkn, stats)
        self.count += 1

    def startGame(self):
        if not self.isrunning:
            return
        iterator = PositionableSequenceIterator(
            [[a, b] for a, b in zip(iconsStart, iconNames)]
        )
        if not self.isrunning:
            return
        for i in iterator:
            if not self.isrunning:
                return
            icon = i[0]
            name = i[1]
            if icon == r"PaladinMainbot_pngs\3Error.png":
                self.current = i
                try:
                    s_width, s_height = pyautogui.size()
                    siz_x, siz_y = Image.open(icon).size
                    image = Image.open(icon).resize(
                        (int(siz_x * (s_width / 1920)), int(siz_y * (s_height / 1080))),
                        Image.ANTIALIAS,
                    )
                    pyautogui.click(
                        pyautogui.center(
                            pyautogui.locateOnScreen(
                                image,
                                confidence=0.9,
                            )
                        )
                    )
                    pyautogui.doubleClick()
                    self.print_to_GUI(f"Found {name}")
                except:
                    continue
            elif icon == r"PaladinMainbot_pngs\5Champlockin.png":
                if not self.isrunning:
                    return
                flag = True
                printing = True
                while flag:
                    if not self.isrunning:
                        return
                    try:
                        self.pickChampionIcon()
                    except:
                        if printing:
                            self.print_to_GUI(f"Waiting to choose selected champion")
                        try:
                            s_width, s_height = pyautogui.size()
                            siz_x, siz_y = Image.open(self.current).size
                            image = Image.open(self.current).resize(
                                (
                                    int(siz_x * (s_width / 1920)),
                                    int(siz_y * (s_height / 1080)),
                                ),
                                Image.ANTIALIAS,
                            )
                            pyautogui.click(
                                pyautogui.center(
                                    pyautogui.locateOnScreen(
                                        image,
                                        confidence=0.9,
                                    )
                                )
                            )
                            pyautogui.doubleClick()
                            self.print_to_GUI(f"Found error button")
                        except:
                            if printing:
                                self.print_to_GUI(f"No Error till now")
                                printing = False
                            continue
                        time.sleep(0.5)
                    else:
                        flag = False
                        time.sleep(0.5)
                flag = True
                while flag:
                    try:
                        s_width, s_height = pyautogui.size()
                        siz_x, siz_y = Image.open(icon).size
                        image = Image.open(icon).resize(
                            (
                                int(siz_x * (s_width / 1920)),
                                int(siz_y * (s_height / 1080)),
                            ),
                            Image.ANTIALIAS,
                        )
                        pyautogui.click(
                            pyautogui.center(
                                pyautogui.locateOnScreen(
                                    image,
                                    confidence=0.70,
                                )
                            )
                        )
                        pyautogui.doubleClick()
                        self.print_to_GUI(f"Found {name}")
                    except:
                        self.print_to_GUI(f"Waiting for {name}")
                    else:
                        flag = False
            else:
                try:
                    s_width, s_height = pyautogui.size()
                    siz_x, siz_y = Image.open(icon).size
                    image = Image.open(icon).resize(
                        (
                            int(siz_x * (s_width / 1920)),
                            int(siz_y * (s_height / 1080)),
                        ),
                        Image.ANTIALIAS,
                    )
                    pyautogui.click(
                        pyautogui.center(
                            pyautogui.locateOnScreen(
                                image,
                                confidence=0.70,
                            )
                        )
                    )
                    pyautogui.doubleClick()
                    self.print_to_GUI(f"Found {name}")
                except:
                    self.print_to_GUI(f"Waiting for {name}")
                    iterator.pos = iterator.pos if iterator.pos > 0 else 0
                    time.sleep(0.5)
            time.sleep(0.5)
        time.sleep(0.5)
        self.print_to_GUI(f"Started Game")
        time.sleep(3)

    def pickChampionIcon(self):
        try:
            s_width, s_height = pyautogui.size()
            siz_x, siz_y = Image.open(self.championIcon).size
            image = Image.open(self.championIcon).resize(
                (
                    int(siz_x * (s_width / 1920)),
                    int(siz_y * (s_height / 1080)),
                ),
                Image.ANTIALIAS,
            )
            pyautogui.click(
                pyautogui.center(
                    pyautogui.locateOnScreen(
                        image,
                        confidence=0.9,
                    )
                )
            )
            pyautogui.doubleClick()
            self.print_to_GUI(f"Found {champion[0] + champion[1:].lower()}")
        except:
            raise Exception("Champion not found")

    def antiAFKGrover(self):
        pyautogui.click()
        pyautogui.doubleClick()
        pyautogui.press("f")
        pyautogui.click()
        pyautogui.doubleClick()
        time.sleep(1)
        pyautogui.press("q")
        pyautogui.click()
        pyautogui.doubleClick()
        time.sleep(1)
        pyautogui.press("e")
        pyautogui.click()
        pyautogui.doubleClick()
        time.sleep(1)
        pyautogui.click()
        pyautogui.click()
        pyautogui.doubleClick()
        pyautogui.doubleClick()
        pyautogui.keyDown("a")
        time.sleep(1)
        pyautogui.keyUp("a")
        time.sleep(1)
        pyautogui.keyDown("s")
        time.sleep(1)
        pyautogui.keyUp("s")
        pyautogui.keyDown("w")
        pyautogui.keyDown("a")
        time.sleep(2)
        pyautogui.keyUp("w")
        pyautogui.keyUp("a")
        pyautogui.click()
        pyautogui.doubleClick()
        pyautogui.click()
        pyautogui.keyUp("d")
        time.sleep(1)
        pyautogui.keyUp("s")
        time.sleep(1)
        pyautogui.keyDown("d")
        pyautogui.keyDown("s")
        pyautogui.click()
        pyautogui.doubleClick()

    def stopLoop(self):
        if self.isrunning:
            self.isrunning = False
            self.stop_event.set()
            self.loopThread = None
            self.stage = "stop"
            self.print_to_GUI("Bot stopping...")
            del self

    def startLoop(self) -> bool:
        """
        Main loop of the bot which goes through the stages and does its necessary action
        """
        if champion == None:
            self.print_to_GUI("Please select a champion to continue", "warning")
            self.stopLoop()
            return False
        if not self.isrunning:
            self.stop_event.clear()
            self.isrunning = True
            self.loopThread = threading.Thread(target=self.actual_loop)
            self.loopThread.start()
            self.print_to_GUI("Bot started")
            return True
        return False

    def startLoopTrial(self) -> bool:
        """
        Main loop of the bot which goes through the stages and does its necessary action
        """
        if champion == None:
            self.print_to_GUI("Please select a champion to continue", "warning")
            self.stopLoop()
            return False
        if not self.isrunning:
            self.stop_event.clear()
            self.isrunning = True
            self.loopThread = threading.Thread(target=self.actual_loop_trial)
            self.loopThread.start()
            self.print_to_GUI("Bot started")
            return True
        return False

    def get_fortnite_window(self):
        got_windows = gw.getWindowsWithTitle("Paladins")
        for window in got_windows:
            window.restore()
            window.activate()
            time.sleep(1)
            handle = win32gui.GetForegroundWindow()
            pid = win32process.GetWindowThreadProcessId(handle)
            for proc in psutil.process_iter():
                if proc.pid == pid[1]:
                    if proc.name().lower() == "Paladins.exe".lower():
                        rect = win32gui.GetWindowRect(handle)
                        x = rect[0]
                        y = rect[1]
                        w = rect[2] - x
                        h = rect[3] - y
                        self.resizeX = w / 1920
                        self.resizeY = h / 1080

                        return None
                    else:
                        window.minimize()

        self.print_to_GUI("Paladins not open... Stop bot and open paladins", "error")
        raise Exception("Paladins not found")

    def runningchck(self):
        return self.isrunning

    def Redo(self):
        flag = True
        printing = True
        while flag:
            if not self.isrunning:
                return
            try:
                self.pickChampionIcon()
            except:
                if printing:
                    self.print_to_GUI(f"Waiting to choose selected champion")
                try:
                    s_width, s_height = pyautogui.size()
                    siz_x, siz_y = Image.open().size
                    image = Image.open(self.current).resize(
                        (
                            int(siz_x * (s_width / 1920)),
                            int(siz_y * (s_height / 1080)),
                        ),
                        Image.ANTIALIAS,
                    )
                    pyautogui.click(
                        pyautogui.center(
                            pyautogui.locateOnScreen(
                                image,
                                confidence=0.9,
                            )
                        )
                    )
                    pyautogui.doubleClick()
                    self.print_to_GUI(f"Found error button")
                except:
                    if printing:
                        self.print_to_GUI(f"No Error till now")
                        printing = False
                    continue
                time.sleep(0.5)
            else:
                flag = False
                time.sleep(0.5)

    def inGameAndRequeue(self):
        flag = True
        while flag:
            if not self.isrunning:
                return
            try:
                s_width, s_height = pyautogui.size()
                siz_x, siz_y = Image.open(iconRequeue).size
                image = Image.open(iconRequeue).resize(
                    (
                        int(siz_x * (s_width / 1920)),
                        int(siz_y * (s_height / 1080)),
                    ),
                    Image.ANTIALIAS,
                )
                pyautogui.click(
                    pyautogui.center(
                        pyautogui.locateOnScreen(
                            image,
                            confidence=0.9,
                        )
                    )
                )
                pyautogui.doubleClick()
                self.print_to_GUI(f"Found re-queue button")
            except:
                self.print_to_GUI(f"Anti-AFK started, waiting for next match")
                if not self.isrunning:
                    return
                self.antiAFKGrover()
                time.sleep(2)
            else:
                flag = False
        time.sleep(2)

    def actual_loop_trial(self):
        self.get_fortnite_window()
        time.sleep(2)
        self.startGame()
        time.sleep(2)
        if not self.isrunning:
            return
        self.pickChampion()
        self.inGameAndRequeue()
        if self.isrunning:
            self.print_to_GUI(f"Game #{self.count}", "control")
            self.count += 1
        elif not self.isrunning:
            return
        self.print_to_GUI(f"Trial loop ended... stopping bot", "warning")
        self.stopLoop()

    def actual_loop(self):
        self.updateData()
        # self.get_fortnite_window()
        time.sleep(2)
        self.firstGame()
        time.sleep(2)
        while True:
            if not self.isrunning:
                return
            self.updateData()
            self.Redo()
            self.pickChampion()
            self.inGameAndRequeue()
            if self.isrunning:
                self.print_to_GUI(f"Game #{self.count}", "control")
                self.count += 1
            elif not self.isrunning:
                return

            if self.pbBool and self.statsSSBool and self.isrunning:
                stats = f"./screenshots/screenshot_{self.count}.png"
                pyautogui.screenshot(stats)
                self.send_image_pushbullet(self.pbAccTkn, stats)

            elif self.statsSSBool and self.isrunning:
                stats = f"./screenshots/screenshot_{self.count}.png"
                pyautogui.screenshot(stats)

            elif self.pbBool and self.isrunning:
                stats = f"./pushbullet/screenshot_{self.count}.png"
                pyautogui.screenshot(stats)
                self.send_image_pushbullet(self.pbAccTkn, stats)

        """flag = True
        while True:
            if not self.isrunning:
                return
            try:
                pyautogui.click(
                    pyautogui.center(pyautogui.locateOnScreen(steam, confidence=0.9))
                )
                self.print_to_GUI("Clicking on Steam")
                time.sleep(3)
                break
            except:
                if flag:
                    self.print_to_GUI("No Steam open")
                    self.print_to_GUI("Waiting steam to open...")
                    flag = False
                time.sleep(10)
        """
        """self.stage = check_stage(self.buttons, lambda: self.runningchck())
        prevstage = ""
        stagecount = 0
        ingamecount = 0
        while self.isrunning:
            print(self.stage)
            if not self.isrunning:
                break
            if self.stage == "lobby":
                if self.tier == 0 and self.numberGames >= 1:
                    self.print_to_GUI(
                        "Trial has ended, please open discord link to register:  https://discord.gg/"
                    )
                    break
                self.print_to_GUI("Looking for play button")
                if check_btns(stage_btns[self.stage], lambda: self.runningchck()):
                    btnlist["play_button"].click()
                    self.print_to_GUI("Play button clicked (waiting for game to start)")
                    self.print_to_GUI(f"Game #{self.numberGames+1}", "control")
                    time.sleep(30)
                    self.stage = "in-bus"
                else:
                    self.stage = "claim-rewards"

            elif self.stage == "in-bus":
                if check_btns(stage_btns["pre-game"], lambda: self.runningchck()):
                    self.print_to_GUI("In pre-game lobby waiting for bus")
                if check_btns(stage_btns[self.stage], lambda: self.runningchck()):
                    time.sleep(12)
                    self.print_to_GUI("Waiting to jump out of the bus")
                    self.numberGames += 1
                    if self.access_level > 0:
                        pyautogui.press("b")
                        self.print_to_GUI("Thanking the bus driver :)")
                    time.sleep(7)
                    # self.stage = "in-jump"
                if check_btns(stage_btns["in-jump"], lambda: self.runningchck()):
                    jumpTime = random.choice(range(self.jumpSecs[0], self.jumpSecs[1]))
                    self.print_to_GUI(f"Jumping out after {jumpTime} seconds")
                    time.sleep(jumpTime)
                    self.print_to_GUI("Jumped out")
                    pyautogui.press("space")
                    time.sleep(1)
                    pyautogui.press("l")
                    pyautogui.press("space")
                    if self.landInTreeBool:
                        if pyautogui.size() == (1920, 1080):
                            self.print_to_GUI("Navigating towards the nearest location")
                            pyautogui.press("space")
                            self.player_mover.land_at_closest_loc()
                            self.print_to_GUI("Location reached")
                        else:
                            self.print_to_GUI(
                                "Screen is not 1920x1080 cannot land on location"
                            )
                    else:
                        time.sleep(60)
                    self.stage = "in-game"
                else:
                    time.sleep(1)

            elif self.stage == "in-game":
                if self.firstInGame:
                    self.print_to_GUI("Waiting to die")
                    self.print_to_GUI("Activating Anti-AFK")
                    self.waitToCrouchTS = datetime.datetime.now().timestamp()
                    self.firstInGame = False
                if self.crouched != True:
                    if datetime.datetime.now().timestamp() - self.waitToCrouchTS > 30.0:
                        pyautogui.press("ctrl")
                        self.print_to_GUI("Crouching")
                        self.crouched = True
                self.antiAFK()
                time.sleep(10)
                self.stage = "post-game"
                if prevstage == "in-game":
                    ingamecount += 1
                if ingamecount > 20:
                    self.print_to_GUI("Bot might be in loop re-checking stage")
                    self.stage = check_stage(self.buttons, lambda: self.runningchck())
                    ingamecount = 0

            elif self.stage == "post-game":
                if check_btns(stage_btns[self.stage], lambda: self.runningchck()):
                    self.print_to_GUI("Returning to lobby")
                    if self.pbBool and self.takeScreenshot:
                        stats = f"./screenshots/screenshot_{self.numberGames}.png"
                        pyautogui.screenshot(stats)
                        self.takeScreenshot = False
                        self.send_image_pushbullet(self.pbAccTkn, stats)
                    btnlist["return_button"].click()
                    self.stage = "claim-rewards"
                else:
                    self.stage = "in-game"

            elif self.stage == "claim-rewards":
                btns = check_btns(stage_btns[self.stage], lambda: self.runningchck())
                if btns:
                    self.print_to_GUI("Claiming rewards")
                    for btnnn in btns:
                        if btnlist[btnnn].cords is not None:
                            btnlist[btnnn].click()
                    self.stage = "lobby"
                else:
                    self.stage = "lobby"

            elif self.stage == "stop":
                self.print_to_GUI("Bot stopped")

            elif self.stage == None:
                self.stage = check_stage(self.buttons, lambda: self.runningchck())

            if self.stage == prevstage:
                stagecount += 1
            else:
                prevstage = self.stage
                stagecount = 0

            if stagecount > 30:
                self.print_to_GUI("Stuck in loop")
                self.stage = check_stage(self.buttons, lambda: self.runningchck())
                stagecount = 0 """
