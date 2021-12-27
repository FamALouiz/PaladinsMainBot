from typing import Sequence
import os, pyautogui
from PIL import Image


class button:
    def __init__(
        self,
        img_path: str,
        cords: tuple[int] = None,
    ) -> None:
        self.img_path = img_path
        self.image = Image.open(img_path)
        self.cords = cords

    def resizeimage(self):
        s_width, s_height = pyautogui.size()
        siz_x, siz_y = self.image.size
        self.image = self.image.resize(
            (int(siz_x * (s_width / 1920)), int(siz_y * (s_height / 1080))),
            Image.ANTIALIAS,
        )

    def click(self):
        pyautogui.moveTo(self.cords)
        pyautogui.click()  # DEV click


# list all png files in icons directory
path = "./icons"
iconlist = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".png")]

btnlist = {}
for btn in iconlist:
    btn_name = btn.split("/")[-1].split(".")[0].split("icons\\")[1]
    btnlist.update({btn_name: button(btn)})

stage_btns = {
    "lobby": ["play_button"],
    "pre-game":["clock_icon_square"],
    "in-bus": ["bus_icon_square"],
    "in-jump": ["jump_icon_square"],
    "in-game": ["storm_icon_square", "ingame_clock_square", "ingame_clock_square2"],
    "claim-rewards": ["collect_button", "collect_button_next"],
    "post-game": ["return_button", "esc_button"],
}
