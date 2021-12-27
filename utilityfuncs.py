import time
from typing import Optional

import psutil
import pyautogui
import pygetwindow as gw
import win32gui
import win32process
from PIL import Image

from icons import btnlist

handle: Optional[int] = None
window: Optional[gw.Window] = None
pid: Optional[int] = None


def get_fortnite_window() -> None:
    global handle, window, pid
    got_windows = gw.getWindowsWithTitle("Fortnite")
    for window in got_windows:
        window.restore()
        window.activate()
        time.sleep(1)
        handle = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(handle)
        for proc in psutil.process_iter():
            if proc.pid == pid[1]:
                if proc.name().lower() == "FortniteClient-Win64-Shipping.exe".lower():
                    return None
                else:
                    window.minimize()
    raise Exception("No fortnite window found")


def isfortnite():
    global handle, window, pid
    if handle != win32gui.GetForegroundWindow():
        print("not fortnite window")
        print("opening fortnite")
        get_fortnite_window()
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


def clickbtn(btn, img, grayscale=False):
    conf = 1.0
    while conf > 0.75:
        cords = pyautogui.locate(btn, img, grayscale=grayscale, confidence=conf)
        if cords:
            pyautogui.moveTo(
                pos_resized(x=cords[0] + cords[2] / 2, y=cords[1] + cords[3] / 2)
            )
            print("conf:", conf)
            pyautogui.click()  # DEV click
            return
        else:
            conf -= 0.05
    else:
        raise Exception("Could not find button")


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
        # elif "bus_icon_square" in found_btns:
        #     return "in-bus"
        elif "jump_icon_square" in found_btns:
            return "in-jump"
        elif "clock_icon_square" in found_btns or "storm_icon_square" in found_btns:
            return "in-game"
        elif "return_button" in found_btns:
            return "post-game"
        elif "claim_button" in found_btns or "collect_button_next" in found_btns:
            return "claim-rewards"


def check_btns(buttons: list, isrunning) -> list:
    global handle, window, pid
    found_btns = []
    img = screenshot_resize("./screenshot.png")
    for name in buttons:
        btn = btnlist[name]
        if not isrunning():
            return []
        cords = findbtn(btn.image, img)
        if cords is not None:
            btn.cords = pos_resized(
                x=(cords[0] + cords[2] / 2), y=(cords[1] + cords[3] / 2)
            )
            btn.found = True
            print(f"Found {name}")
            found_btns.append(name)
    return found_btns


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
