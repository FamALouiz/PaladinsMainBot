import time
from typing import Optional

import psutil
import pyautogui
import pyscreeze
import pygetwindow as gw
import win32gui
import win32process
from PIL import Image


def get_fortnite_window():
    got_windows = gw.getWindowsWithTitle("Fortnite")
    for window in got_windows:
        window.restore()
        window.activate()

        time.sleep(1)
        handle = win32gui.GetForegroundWindow()
        PId = win32process.GetWindowThreadProcessId(handle)
        for proc in psutil.process_iter():
            if proc.pid == PId[1]:
                if proc.name().lower() == "FortniteClient-Win64-Shipping.exe".lower():
                    return handle, window, PId
                else:
                    window.minimize()
    raise Exception("No fortnite window found")


def isfortnite(handle):
    return handle == win32gui.GetForegroundWindow()


def screenshot_rezise(window, handle, path):
    if not isfortnite(handle):
        print("not fortnite window")
        window, handle, path = get_fortnite_window()
    # screenshot the display
    img: Image.Image = pyautogui.screenshot(path)
    print(type(img))
    # open image
    # img = Image.open(path)
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
    while conf > 0.25:
        cords = pyautogui.locate(btn, img, confidence=conf)
        if cords:
            pyautogui.moveTo(x=cords[0] + cords[2] / 2, y=cords[1] + cords[3] / 2)
            # pyautogui.click() # DEV click
        else:
            conf -= 0.05
