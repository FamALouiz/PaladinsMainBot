from typing import Sequence
import os, pyautogui
from PIL import Image


class button:
    def __init__(
        self,
        img_path: str,
        cords: Sequence[int] = None,
        found: bool = False,
    ) -> None:
        self.img_path = img_path
        self.image = Image.open(img_path)
        self.cords = cords
        self.found = found

    def resizeimage(self):
        s_width, s_height = pyautogui.size()
        siz_x, siz_y = self.image.size
        self.image = self.image.resize((int(siz_x * (s_width / 1920)), int(siz_y * (s_height / 1080))), Image.ANTIALIAS)


# list all png files in icons directory
path = "./icons"
iconlist = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".png")]

btnlist = {}
for btn in iconlist:
    btn_name = btn.split("/")[-1].split(".")[0].split("icons\\")[1]
    btnlist.update({btn_name: button(btn)})

print(btnlist)
