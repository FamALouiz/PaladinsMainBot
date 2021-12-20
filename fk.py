import time

import psutil
import pyautogui
import pygetwindow as gw
import win32gui
import win32process
from PIL import Image

# get fortnite window
path = './screenshot.png'
fortnite = None
got_windows = gw.getWindowsWithTitle('Fortnite')
for window in got_windows:
    window.restore()
    window.activate()

    time.sleep(1)
    handle = win32gui.GetForegroundWindow()
    PId = win32process.GetWindowThreadProcessId(handle)
    for proc in psutil.process_iter():
        if proc.pid == PId[1]:
            if proc.name().lower() == "FortniteClient-Win64-Shipping.exe".lower():
                fortnite = window
                break
            else:
                window.minimize()

pyautogui.screenshot(path)
# open image
img = Image.open(path)
# get screen resolution size
s_width, s_height = pyautogui.size()

fx, fy = fortnite.topleft
# crop fortnite window

img = img.crop((fortnite.topleft[0], fortnite.topleft[1], fortnite.bottomright[0], fortnite.bottomright[1]))
img.save(path)
img.resize((s_width, s_height))
cords = pyautogui.locate('./icons/FortniteClient-Win64-Shipping_0esI0YTdCc.png', img, confidence=0.7)
pyautogui.moveTo(x=cords[0] + fx + cords[2] / 2, y=cords[1] + fy + cords[3] / 2)
