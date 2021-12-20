import numpy as np, cv2, os, sys


class ButtonsAndIcons:
    def __init__(self):
        self.esc_buttons = []
        btn = cv2.imread(self.resource_path("esc_button.png"))
        self.esc_buttons = self.init_scaled_imgs(btn)
        self.continue_blue_buttons = []
        btn = cv2.imread(self.resource_path("continue_blue_button.png"))
        self.continue_blue_buttons = self.init_scaled_imgs(btn)
        self.collect_buttons = []
        btn = cv2.imread(self.resource_path("collect_button.png"))
        self.collect_buttons = self.init_scaled_imgs(btn)
        self.collect_next_buttons = []
        btn = cv2.imread(self.resource_path("collect_button_next.png"))
        self.collect_next_buttons = self.init_scaled_imgs(btn)
        self.play_buttons = []
        btn = cv2.imread(self.resource_path("play_button.png"))
        self.play_buttons = self.init_scaled_imgs(btn)
        self.ready_buttons = []
        btn = cv2.imread(self.resource_path("ready_button.png"))
        self.ready_buttons = self.init_scaled_imgs(btn)
        self.return_buttons = []
        btn = cv2.imread(self.resource_path("return_button.png"))
        self.return_buttons = self.init_scaled_imgs(btn)
        self.bus_icons = []
        btn = cv2.imread(self.resource_path("bus_icon_square.png"))
        self.bus_icons = self.init_scaled_imgs(btn)
        self.jump_icons = []
        btn = cv2.imread(self.resource_path("jump_icon_square.png"))
        self.jump_icons = self.init_scaled_imgs(btn)
        self.clock_icons = []
        btn = cv2.imread(self.resource_path("clock_icon_square.png"))
        self.clock_icons = self.init_scaled_imgs(btn)
        self.team_alive_icons = []
        btn = cv2.imread(self.resource_path("team_alive_icon.png"))
        self.team_alive_icons = self.init_scaled_imgs(btn)
        self.player_cursor_icon = cv2.imread(
            self.resource_path("player_cursor.png"), cv2.IMREAD_UNCHANGED
        )
        # # Salem Google Chrome Test
        # self.google_icon = []
        # btn = cv2.imread(self.resource_path("google_home.png"))
        # self.google_icon = self.init_scaled_imgs(btn)

    def init_scaled_imgs(self, img):
        buttons = []
        for scale in np.arange(0.5, 1.2, 0.02):
            resized = cv2.resize(img, (0, 0), fx=scale, fy=scale)
            buttons.append(resized)

        return buttons

    def resource_path(self, rel_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, rel_path)
        else:
            return os.path.join("../icons", rel_path)


if __name__ == "__main__":
    pass
