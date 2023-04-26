import numpy as np, cv2

try:
    from cv2 import cv2
except ImportError:
    pass

import os, sys, time, pyautogui, keyboard, win32gui, win32con, random, datetime, asyncio, threading, winreg
from PIL import ImageGrab
from tkinter import *
import requests
from my_icons import ButtonsAndIcons
from player_movement import PlayerMovement


class MainBotLoop:
    def __init__(
        self,
        listBoxLogger,
        jumpSecs,
        statsSSBool,
        pbBool,
        pbAccTkn,
        landInTreeBool,
        tier=0,
    ):
        self.access_level = tier
        self.print_area = listBoxLogger
        self.jumpSecs = jumpSecs
        self.statsSSBool = statsSSBool
        self.pbBool = pbBool
        self.pbAccTkn = pbAccTkn
        self.landInTreeBool = landInTreeBool
        self.running = False
        self.stop_event = threading.Event()
        self.interval = 0.5
        self.env = "production"
        self.work_mode = "lobby"
        self.loopCount = 0
        self.maxLoops = -1
        self.escAndContCount = 1
        self.look_for_jump = True
        self.lastMessage = ""
        self.return_loc = None
        self.screenshot = []
        self.matched = []
        try:
            if self.access_level == 0:
                raise WindowsError
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, "Software\\FortBot", 0, winreg.KEY_READ
            )
            value, _ = winreg.QueryValueEx(registry_key, "esc_button_scale")
            self.esc_button_scale = int(value)
            value, _ = winreg.QueryValueEx(registry_key, "continue_button_scale")
            self.continue_button_scale = int(value)
            value, _ = winreg.QueryValueEx(registry_key, "collect_button_scale")
            self.collect_button_scale = int(value)
            value, _ = winreg.QueryValueEx(registry_key, "play_button_scale")
            self.play_button_scale = int(value)
            value, _ = winreg.QueryValueEx(registry_key, "return_button_scale")
            self.return_button_scale = int(value)
            value, _ = winreg.QueryValueEx(registry_key, "icons_scale")
            self.icons_scale = int(value)
            value, _ = winreg.QueryValueEx(registry_key, "team_alive_scale")
            self.team_alive_scale = int(value)
            winreg.CloseKey(registry_key)
        except WindowsError:
            if self.access_level > 0:
                self.print_to_GUI("Error reading saved resolution", "error")
            self.esc_button_scale = -1
            self.continue_button_scale = -1
            self.collect_button_scale = -1
            self.play_button_scale = -1
            self.return_button_scale = -1
            self.icons_scale = -1
            self.team_alive_scale = -1

        self.bai = ButtonsAndIcons()
        self.player_mover = PlayerMovement(self.bai.player_cursor_icon)
        self.serverPingTS = datetime.datetime.now().timestamp()
        self.waitToCrouchTS = datetime.datetime.now().timestamp()
        self.crouchedAfterFall = False

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

    def enumCallback(self, hwnd, name):
        if name in str(win32gui.GetWindowText(hwnd)).lower():
            self.fortniteHandle = hwnd

    def startLoop(self, enableStart):
        if not self.running:
            self.fortniteHandle = None
            win32gui.EnumWindows(self.enumCallback, "fortnite")
            if self.fortniteHandle is not None:
                if self.env != "development":
                    win32gui.ShowWindow(self.fortniteHandle, win32con.SW_SHOWDEFAULT)
                    win32gui.BringWindowToTop(self.fortniteHandle)
                    win32gui.SetForegroundWindow(self.fortniteHandle)
                    self.print_to_GUI("Fortnite brought to foreground")
                    self.fortniteHandle = None
            if self.access_level == 0:
                self.maxLoops = random.randint(1, 3)
                self.jumpSecs = (0, 25)
            self.stop_event.clear()
            self.loopThread = threading.Thread(
                target=(self.loopClosure), args=[enableStart]
            )
            self.loopThread.start()
            return True

    def loopClosure(self, enableStartButton):
        self.print_to_GUI(
            "Jump delay set between %.1f and %.1f seconds"
            % (self.jumpSecs[0], self.jumpSecs[1]),
            "control",
        )
        self.print_to_GUI("Bot started", "control")
        self.running = True
        self.modeResetTimer = time.time()
        while not self.stop_event.is_set():
            self.mainLoop()
            self.stop_event.wait(self.interval)

        self.print_to_GUI("Bot stopped", "control")
        self.running = False
        enableStartButton()

    def stopLoop(self):
        if self.running:
            self.print_to_GUI("Stopping bot", "warning")
            self.stop_event.set()
            self.loopThread = None
            win32gui.EnumWindows(self.enumCallback, "fortbot")
            if self.fortniteHandle is not None:
                win32gui.ShowWindow(self.fortniteHandle, win32con.SW_SHOWDEFAULT)
                win32gui.BringWindowToTop(self.fortniteHandle)
                win32gui.SetForegroundWindow(self.fortniteHandle)
                self.fortniteHandle = None

    def mainLoop(self):
        timestampNow = datetime.datetime.now().timestamp()
        if timestampNow - self.serverPingTS > 7200:
            self.serverPingTS = timestampNow
            try:
                requests.get("https://fortbot-server.herokuapp.com")
            except:
                pass

        if time.time() - self.modeResetTimer > 1800:
            self.reset_variables()
        handle = win32gui.GetForegroundWindow()
        windowName = str(win32gui.GetWindowText(handle))
        if "fortnite" not in windowName.lower():
            shortwn = windowName[: 30 if len(windowName) > 30 else len(windowName)]
            if shortwn != windowName:
                shortwn += " ..."
            self.print_to_GUI(
                "Active window: '" + shortwn + "', please open Fortnite", "warning"
            )
            if self.env != "development":
                time.sleep(0.5)
                return
        try:
            bbox = win32gui.GetWindowRect(handle)
        except:

            return
        else:
            self.screenshot = ImageGrab.grab(bbox)
            self.screenshot = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_RGB2BGR)
            ss_height, ss_width, _ = self.screenshot.shape
            loc = None
        if self.work_mode == "lobby":
            self.print_to_GUI("Looking for Play_button")
            if self.escAndContCount % 5 == 0:
                area_bbox = (0, ss_height, 0, ss_width)
                loc = self.button_location_scale(
                    self.bai.esc_buttons,
                    self.esc_button_scale,
                    area_bbox,
                    "esc_button_scale",
                )
                if loc is not None:
                    if len(loc) == 3:
                        self.esc_button_scale = loc[2]
                        self.print_to_GUI(
                            "Esc_button scale set to: " + str(self.esc_button_scale)
                        )
                if self.click_button_in_ss(bbox, loc):
                    self.print_to_GUI("Esc_button clicked (closing popup or menu)")
                area_bbox = (
                    int(ss_height / 2),
                    ss_height,
                    int(ss_width / 3),
                    int(2 * ss_width / 3),
                )
                loc = self.button_location_scale(
                    (self.bai.continue_blue_buttons),
                    (self.continue_button_scale),
                    area_bbox,
                    "continue_button_scale",
                    threshold=0.7,
                )
                if loc is not None:
                    if len(loc) == 3:
                        self.continue_button_scale = loc[2]
                        self.print_to_GUI(
                            "Continue_button scale set to: "
                            + str(self.continue_button_scale)
                        )
                if self.click_button_in_ss(bbox, loc):
                    self.print_to_GUI(
                        "Continue_button clicked (closing matchmaking error)"
                    )
                area_bbox = (
                    int(3 * ss_height / 4),
                    ss_height,
                    int(ss_width / 2),
                    int(4 * ss_width / 5),
                )
                while True:
                    pyautogui.moveTo(100, 100)
                    loc = self.button_location_scale(
                        (self.bai.collect_next_buttons),
                        (self.collect_button_scale),
                        area_bbox,
                        "collect_button_scale",
                        threshold=0.7,
                    )
                    if loc is not None:
                        if len(loc) == 3:
                            self.collect_button_scale = loc[2]
                            self.print_to_GUI(
                                "Collect_button scale set to: "
                                + str(self.collect_button_scale)
                            )
                    if self.click_button_in_ss(bbox, loc):
                        self.print_to_GUI("Next_button clicked (collecting rewards)")
                    else:
                        pyautogui.moveTo(100, 100)
                        time.sleep(1.0)
                        break
                    time.sleep(1.0)

                loc = self.button_location_scale(
                    (self.bai.collect_buttons),
                    (self.collect_button_scale),
                    area_bbox,
                    "collect_button_scale",
                    threshold=0.7,
                )
                if loc is not None:
                    if len(loc) == 3:
                        self.collect_button_scale = loc[2]
                        self.print_to_GUI(
                            "Collect_button scale set to: "
                            + str(self.collect_button_scale)
                        )
                if self.click_button_in_ss(bbox, loc):
                    self.print_to_GUI("Collect_button clicked (collecting rewards)")
                self.escAndContCount = 0
            area_bbox = (int(ss_height / 2), ss_height, int(5 * ss_width / 6), ss_width)
            loc = self.button_location_scale(
                self.bai.play_buttons,
                self.play_button_scale,
                area_bbox,
                "play_button_scale",
            )
            if loc is not None:
                if len(loc) == 3:
                    self.play_button_scale = loc[2]
                    self.print_to_GUI(
                        "Play_button scale set to: " + str(self.play_button_scale)
                    )
            if self.click_button_in_ss(bbox, loc):
                self.print_to_GUI("Play_button clicked (starting game)")
            loc = self.button_location_scale(
                self.bai.ready_buttons,
                self.play_button_scale,
                area_bbox,
                "play_button_scale",
            )
            if loc is not None:
                if len(loc) == 3:
                    self.play_button_scale = loc[2]
                    self.print_to_GUI(
                        "Ready_button scale set to: " + str(self.play_button_scale)
                    )
            if self.click_button_in_ss(bbox, loc):
                self.print_to_GUI("Ready_button clicked (starting game)")
                pyautogui.moveTo(10, 10)
            area_bbox = (
                int(ss_height / 4),
                int(ss_height / 2),
                int(4 * ss_width / 5),
                ss_width,
            )
            if (
                self.is_icon_present(self.bai.bus_icons, area_bbox, 0.85)
                or self.is_icon_present(self.bai.jump_icons, area_bbox, 0.75)
                or self.is_icon_present(self.bai.clock_icons, area_bbox)
            ):
                self.work_mode = "ingame"
                self.modeResetTimer = time.time()
                self.print_to_GUI("Current location: ingame")
            self.escAndContCount += 1
        if self.work_mode == "ingame":
            if self.look_for_jump:
                self.print_to_GUI("Waiting to jump out of the bus")
                area_bbox = (
                    int(ss_height / 4),
                    int(ss_height / 2),
                    int(4 * ss_width / 5),
                    ss_width,
                )
                jump_icon = self.is_icon_present(self.bai.jump_icons, area_bbox, 0.75)
                if jump_icon:
                    if self.access_level > 0:
                        pyautogui.press("b")
                        self.print_to_GUI("Thanking the bus driver :)")
                    clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
                    jump_delay = (
                        clamp(np.abs(np.random.normal(loc=2.0, scale=0.8)), 0, 4)
                        * ((self.jumpSecs[1] - self.jumpSecs[0]) / 4)
                        + self.jumpSecs[0]
                    )
                    self.print_to_GUI(
                        "Jumping out after " + "%.1f" % jump_delay + " seconds"
                    )
                    time.sleep(jump_delay)
                    pyautogui.press("space")
                    self.print_to_GUI("Jumped out")
                    if self.landInTreeBool:
                        self.print_to_GUI("Navigating towards the nearest tree")
                        pyautogui.press("space")
                        keyboard.press("space")
                        pyautogui.press("m")
                        time.sleep(2.0)
                        self.player_mover.land_at_closest_loc()
                        self.print_to_GUI("Tree reached")
                        self.waitToCrouchTS = datetime.datetime.now().timestamp()
                    self.look_for_jump = False
            else:
                if not self.crouchedAfterFall:
                    if datetime.datetime.now().timestamp() - self.waitToCrouchTS > 80.0:
                        pyautogui.press("ctrl")
                        self.crouchedAfterFall = True
                    self.print_to_GUI("Waiting to die")
                    area_bbox = (
                        int(3 * ss_height / 4),
                        ss_height,
                        int(3 * ss_width / 4),
                        ss_width,
                    )
                    self.return_loc = self.button_location_scale(
                        self.bai.return_buttons,
                        self.return_button_scale,
                        area_bbox,
                        "return_button_scale",
                        0.6,
                    )
                    if self.return_loc is not None:
                        if len(self.return_loc) == 3:
                            self.return_button_scale = self.return_loc[2]
                            self.print_to_GUI(
                                "Return_button scale set to: "
                                + str(self.return_button_scale)
                            )
                else:
                    if self.return_loc is not None:
                        if any((self.statsSSBool, self.pbBool)):
                            self.print_to_GUI("Waiting to take a screenshot")
                            time.sleep(10.0)
                            try:
                                handle = win32gui.GetForegroundWindow()
                                bbox = win32gui.GetWindowRect(handle)
                                statsSS = ImageGrab.grab(bbox)
                                statsSS = cv2.cvtColor(
                                    np.array(statsSS).astype(np.uint8),
                                    cv2.COLOR_RGB2BGR,
                                )
                                if self.statsSSBool:
                                    folderName = datetime.datetime.fromtimestamp(
                                        time.time()
                                    ).strftime("%Y_%m_%d")
                                    folder_path = os.path.join(
                                        self.main_file_path(), folderName
                                    )
                                    if not os.path.isdir(folder_path):
                                        os.makedirs(folder_path)
                                    ssName = datetime.datetime.fromtimestamp(
                                        time.time()
                                    ).strftime("%H_%M_%S.png")
                                    ss_path = os.path.join(folderName, ssName)
                                    cv2.imwrite(ss_path, statsSS)
                                    self.print_to_GUI("Saved screenshot of Match Stats")
                                if self.pbBool:
                                    cv2.imwrite("screenshot.jpg", statsSS)
                                    self.send_image_pushbullet(
                                        self.pbAccTkn,
                                        "screenshot.jpg",
                                        self.loopCount + 1,
                                    )
                                    os.remove("screenshot.jpg")
                            except RuntimeError:
                                self.print_to_GUI("Unable to save screenshot", "error")

                if self.click_button_in_ss(bbox, self.return_loc):
                    self.reset_variables()
                    self.modeResetTimer = time.time()
                    self.loopCount += 1
                    self.print_to_GUI("Return_button clicked")
                    self.print_to_GUI("Game finished, returning to lobby")
                    self.print_to_GUI("Total games finished: " + str(self.loopCount))
                    if self.maxLoops > -1:
                        if self.loopCount >= self.maxLoops:
                            self.print_to_GUI("Max number of games reached")
                            self.stopLoop()
                    else:
                        time.sleep(1.0)
        if self.work_mode == "dead_weight":
            area_bbox = (0, int(2 * ss_height / 3), int(ss_width / 2), ss_width)
            loc = self.button_location_scale(
                self.bai.team_alive_icons,
                self.team_alive_scale,
                area_bbox,
                "team_alive_scale",
            )
            if loc is not None:
                if len(loc) == 3:
                    self.team_alive_scale = loc[2]
            if loc is None:
                if any((self.statsSSBool, self.pbBool)):
                    self.print_to_GUI("Waiting to take a screenshot")
                    time.sleep(10.0)
                    try:
                        handle = win32gui.GetForegroundWindow()
                        bbox = win32gui.GetWindowRect(handle)
                        statsSS = ImageGrab.grab(bbox)
                        statsSS = cv2.cvtColor(
                            np.array(statsSS).astype(np.uint8), cv2.COLOR_RGB2BGR
                        )
                        if self.statsSSBool:
                            folderName = datetime.datetime.fromtimestamp(
                                time.time()
                            ).strftime("%Y_%m_%d")
                            folder_path = os.path.join(
                                self.main_file_path(), folderName
                            )
                            if not os.path.isdir(folder_path):
                                os.makedirs(folder_path)
                            ssName = datetime.datetime.fromtimestamp(
                                time.time()
                            ).strftime("%H_%M_%S.png")
                            ss_path = os.path.join(folderName, ssName)
                            cv2.imwrite(ss_path, statsSS)
                            self.print_to_GUI("Saved screenshot of Match Stats")
                        if self.pbBool:
                            cv2.imwrite("screenshot.jpg", statsSS)
                            self.send_image_pushbullet(
                                self.pbAccTkn, "screenshot.jpg", self.loopCount + 1
                            )
                            os.remove("screenshot.jpg")
                    except RuntimeError:
                        self.print_to_GUI("Unable to save screenshot", "error")

                    pyautogui.press("esc")
                    time.sleep(1.0)
                    if self.click_button_in_ss(bbox, self.return_loc):
                        self.reset_variables()
                        self.modeResetTimer = time.time()
                        self.loopCount += 1
                        self.print_to_GUI("Return_button clicked")
                        self.print_to_GUI("Game finished, returning to lobby")
                        self.print_to_GUI(
                            "Total games finished: " + str(self.loopCount)
                        )
                        if self.maxLoops > -1 and self.loopCount >= self.maxLoops:
                            self.print_to_GUI("Max number of games reached")
                            self.stopLoop()
                        else:
                            time.sleep(1.0)
            else:
                self.print_to_GUI("Waiting for the rest of the party to die")

    def reset_variables(self):
        self.work_mode = "lobby"
        self.look_for_jump = True
        self.crouchedAfterFall = False

    def button_location(self, button, area_bbox, threshold):
        btn_height, btn_width, _ = button.shape
        try:
            self.matched = cv2.matchTemplate(
                (
                    self.screenshot[
                        area_bbox[0] : area_bbox[1], area_bbox[2] : area_bbox[3], :
                    ]
                ),
                button,
                (cv2.TM_CCOEFF_NORMED),
                mask=None,
            )
        except Exception as e:
            print(e)
            _, max_val, _, max_loc = cv2.minMaxLoc(self.matched)
            print(max_val)
            print(threshold)
            if max_val > threshold:
                return (
                    int(area_bbox[2] + max_loc[0] + btn_width / 2),
                    int(area_bbox[0] + max_loc[1] + btn_height / 2),
                    max_val,
                )
            return
        else:
            _, max_val, _, max_loc = cv2.minMaxLoc(self.matched)
            return (
                int(area_bbox[2] + max_loc[0] + btn_width / 2),
                int(area_bbox[0] + max_loc[1] + btn_height / 2),
                max_val,
            )

    def click_button_in_ss(self, bbox, loc, sleep_time=0.3):
        if loc is not None:
            pyautogui.moveTo(bbox[0] + loc[0], bbox[1] + loc[1])
            pyautogui.click()
            time.sleep(sleep_time)
            return True
        else:
            return False

    def button_location_scale(self, buttons, scale, area_bbox, name, threshold=0.8):
        loc = None
        new_scale = -1
        if scale == -1:
            max_val = -1
            i = 0
            for btn in buttons:
                temp_loc = self.button_location(btn, area_bbox, threshold)
                if temp_loc is not None:
                    if temp_loc[2] > max_val:
                        loc = temp_loc
                        max_val = temp_loc[2]
                        new_scale = i
                i += 1

        else:
            loc = self.button_location(buttons[scale], area_bbox, threshold)
        if loc is not None:
            if new_scale != -1:
                key_path = "Software\\FortBot"
                try:
                    registry_key = winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE
                    )
                    winreg.SetValueEx(
                        registry_key, name, 0, winreg.REG_SZ, str(new_scale)
                    )
                    winreg.CloseKey(registry_key)
                except WindowsError:
                    print("Error setting registry entry.")

                return (loc[0], loc[1], new_scale)
            else:
                return (loc[0], loc[1])
        else:
            return

    def is_icon_present(self, buttons, area_bbox, threshold=0.8):
        new_scale = -1
        max_max_val = -1
        if self.icons_scale == -1:
            for idx, btn in enumerate(buttons):
                self.matched = cv2.matchTemplate(
                    (
                        self.screenshot[
                            area_bbox[0] : area_bbox[1], area_bbox[2] : area_bbox[3], :
                        ]
                    ),
                    btn,
                    (cv2.TM_CCOEFF_NORMED),
                    mask=None,
                )
                _, max_val, _, max_loc = cv2.minMaxLoc(self.matched)
                if max_val > threshold and max_val > max_max_val:
                    max_max_val = max_val
                    new_scale = idx

            if max_max_val > threshold:
                self.icons_scale = new_scale
                key_path = "Software\\FortBot"
                try:
                    registry_key = winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE
                    )
                    winreg.SetValueEx(
                        registry_key, "icons_scale", 0, winreg.REG_SZ, str(new_scale)
                    )
                    winreg.CloseKey(registry_key)
                except WindowsError:
                    print("Error setting registry entry.")

                self.print_to_GUI("Icons scale set to: " + str(self.icons_scale))
        else:
            self.matched = cv2.matchTemplate(
                (
                    self.screenshot[
                        area_bbox[0] : area_bbox[1], area_bbox[2] : area_bbox[3], :
                    ]
                ),
                (buttons[self.icons_scale]),
                (cv2.TM_CCOEFF_NORMED),
                mask=None,
            )
            _, max_max_val, _, max_loc = cv2.minMaxLoc(self.matched)
        if max_max_val > threshold:
            return True
        else:
            return False

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

    def main_file_path(self):
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    bot = MainBotLoop(0)
    bot.start()
    bot.mainLoop()
