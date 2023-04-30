import time
from typing import Optional

import psutil
import pyautogui
import pygetwindow as gw
import win32gui
import win32process
from PIL import Image

handle: Optional[int] = None
window: Optional[gw.Window] = None
pid: Optional[int] = None


def get_fortnite_window() -> None:
    global handle, window, pid
    got_windows = gw.getWindowsWithTitle("Paladins (64-bit, DX11)")
    for window in got_windows:
        window.restore()
        window.activate()
        time.sleep(1)
        handle = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(handle)
        for proc in psutil.process_iter():
            if proc.pid == pid[1]:
                if proc.name().lower() == "Paladins.exe".lower():
                    return None
                else:
                    window.minimize()

    raise Exception("No Paladins window found")


def get_steam_window() -> None:
    global handle, window, pid
    got_windows = gw.getWindowsWithTitle("Steam")
    for window in got_windows:
        window.restore()
        window.activate()
        time.sleep(1)
        handle = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(handle)
        for proc in psutil.process_iter():
            if proc.pid == pid[1]:
                if proc.name().lower() == "Steam.exe".lower():
                    return None
                else:
                    window.minimize()
    raise Exception("No Steam window found")


def isfortnite():
    global handle, window, pid
    if handle != win32gui.GetForegroundWindow():
        print("not paladin window")
        print("opening paladins")
        get_fortnite_window()
        time.sleep(4)


def isSteam():
    global handle, window, pid
    if handle != win32gui.GetForegroundWindow():
        print("no steam")
        print("opening steam")
        get_steam_window()
        time.sleep(4)


def screenshot_resize(path):
    global handle, window, pid
    isfortnite()
    # screenshot the display
    img: Image.Image = pyautogui.screenshot()
    # get screen resolution size
    s_width, s_height = pyautogui.size()
    # crop fortnite window
    img = img.crop(
        (
            window.topleft[0],
            window.topleft[1],
            window.bottomright[0],
            window.bottomright[1],
        )
    )
    img = img.resize((s_width, s_height))
    # img.save(path)  # DEV save image
    return img


def clickbtn(image, Region=None, Precision=0.8):
    return None


def check_stage(buttons: dict, isrunning) -> str:
    global handle, window, pid
    found_btns = []
    img = screenshot_resize("./screenshot.png")
    for name, btn in buttons.items():
        if not isrunning():
            return
        if pyautogui.size() != (1920, 1080):
            btn.resizeimage()
        cords = findbtn(btn.image, img)
        if cords is not None:
            btn.cords = pos_resized(
                x=(cords[0] + cords[2] / 2), y=(cords[1] + cords[3] / 2)
            )
            print(f"Found {name}")
            found_btns.append(name)
    if found_btns:
        if "play_button" in found_btns:
            return "lobby"
        elif "bus_icon_square" in found_btns:
            return "in-bus"
        elif "jump_icon_square" in found_btns or "clock_icon_square" in found_btns:
            return "in-bus"
        elif (
            "ingame_clock_square" in found_btns
            or "storm_icon_square" in found_btns
            or "ingame_clock_square2" in found_btns
        ):
            return "in-game"
        elif "return_button" in found_btns:
            return "post-game"
        elif "claim_button" in found_btns or "collect_button_next" in found_btns:
            return "claim-rewards"


def findbtn(btn, img, grayscale=False):
    conf = 1.0
    while conf > 0.74:
        cords = pyautogui.locate(btn, img, grayscale=grayscale, confidence=conf)
        if cords:
            print("conf:", conf)
            return cords
        else:
            conf -= 0.05
    return None


def pos_resized(x, y):
    global handle, window, pid
    s_width, s_height = pyautogui.size()
    w, h = window.size
    if w == s_width and h == s_height:
        return x, y
    windowpos = window.topleft
    x = x * w / s_width + windowpos[0]
    y = y * h / s_height + windowpos[1]
    return x, y
