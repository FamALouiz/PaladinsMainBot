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


def screenshot_resize(path):
    global handle, window, pid
    isfortnite()
    # screenshot the display
    img: Image.Image = pyautogui.screenshot(path)
    # get screen resolution size
    s_width, s_height = pyautogui.size()
    fx, fy = window.topleft
    # crop fortnite window
    img = img.crop(
        (
            window.topleft[0],
            window.topleft[1],
            window.bottomright[0],
            window.bottomright[1],
        )
    )
    img.resize((s_width, s_height))
    img.save(path)  # DEV save image
    return img


def clickbtn(btn, img):
    conf = 1.0
    while conf > 0.5:
        cords = pyautogui.locate(btn, img, confidence=conf)
        if cords:
            pyautogui.moveTo(x=cords[0] + cords[2] / 2, y=cords[1] + cords[3] / 2)
            # pyautogui.click() # DEV click
            return
        else:
            conf -= 0.05
    else:
        raise Exception("Could not find button")


def check_stage(buttons: list) -> str:
    global handle, window, pid
    found_btns = []
    for name, btn in btnlist.items():
        if btn.found:
            continue
        cords = findbtn(btn.img_path, screenshot_resize("./temp.png"))
        if cords:
            btn.cords = cords
            btn.found = True
            print(f"Found {name}")
            found_btns.append(name)
    if found_btns:
        if "play_button" in found_btns:
            return "solo-lobby"
        elif "ready_button" in found_btns:
            return "party-lobby"
        elif "bus_icon_square" in found_btns:
            return "in-bus"
        elif "jump_icon_square" in found_btns:
            return "in-jump"
        elif "clock_icon_square" in found_btns:
            return "in-game"
        elif "return_button" in found_btns:
            return "post-game"
        elif "claim_button" in found_btns:
            return "claim-rewards"
        elif "next_button" in found_btns:
            return "claim-rewards-next"
        elif "continue_blue_button" in found_btns:
            print("continue button found")
            return "continue"


def findbtn(btn, img, grayscale=False):
    conf = 1.0
    while conf > 0.5:
        cords = pyautogui.locate(btn, img, grayscale=grayscale, confidence=conf)
        if cords:
            print("conf:", conf)
            return cords
        else:
            conf -= 0.05
    return None, None, None, None
