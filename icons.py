from typing import Sequence
import os
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


# list all png files in icons directory
path = "./icons"
iconlist = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".png")]

btnlist = {}
for btn in iconlist:
    btn_name = btn.split("/")[-1].split(".")[0].split("icons\\")[1]
    btnlist.update({btn_name: button(btn)})

print(btnlist)
