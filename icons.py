from typing import Sequence
import os, pyautogui
from PIL import Image
import cv2


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


stage_btns = {
    "lobby": ["play_button", "return_button"],
    "pre-game": ["clock_icon_square"],
    "in-bus": ["bus_icon_square"],
    "in-jump": ["jump_icon_square"],
    "in-game": ["storm_icon_square", "ingame_clock_square", "ingame_clock_square2"],
    "claim-rewards": ["collect_button", "collect_button_next"],
    "post-game": ["return_button", "esc_button"],
}
