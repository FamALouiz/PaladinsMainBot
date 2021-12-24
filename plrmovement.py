from random import randint

import autoit
import cv2
import numpy as np
from numpy import floor

from functions import *


class Player:
    x: int
    y: int
    width: int
    height: int
    orientation: int
    crouched: bool
    sprinting: bool
    player_cursor_img: str

    def __init__(self, player_cursor_img: str):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.orientation = 0
        self.crouched = False
        self.sprinting = False
        self.player_cursor_img = player_cursor_img

    @property
    def center(self):
        return self.width / 2, self.height / 2

    @property
    def position(self):
        return self.x, self.y

    def get_current_position(self, ang_range=range(0, 360, 10), minimap=True, map_loc=(0, 0)):
        # if minimap is true meaning that it will be getting the player location from the map
        if not minimap:
            # opens minimap and then takes a screenshot
            pyautogui.press("m")
            print("pressing M")
            autoit.mouse_move(map_loc[0], map_loc[1])
            autoit.mouse_click()
            img: Image.Image = screenshot_resize("./screenshot.png")
            pyautogui.press("m")
            img = cv2.imread("./screenshot.png")
        else:
            # if minimap is false meaning that it will be getting the player orientation from the minimap
            center_cursor = (1754.5, 159.5)  # DEV make dynamic
            # crops the cursor from the minimap for more accurate results
            cursor_size = (
                int(center_cursor[0] - 13.5),
                int(center_cursor[1] - 13.5),
                int(center_cursor[0] + 13.5),
                int(center_cursor[1] + 13.5),
            )
            img: Image.Image = screenshot_resize("./screenshot.png")
            img = img.crop(cursor_size)
            img.save("./screenshot.png")
            img = cv2.imread("./screenshot.png")
        cursor = cv2.imread(self.player_cursor_img)
        width, height = cursor.shape[:2]
        max_val = 0
        rotation = 0
        best_template = None
        best_trans_mask = None
        best_match = None
        boxx = None
        # rotates the player cursor to find the best match
        for i in ang_range:
            M = cv2.getRotationMatrix2D(
                (
                    cursor.shape[1] / 2,
                    cursor.shape[0] / 2,
                ),
                i,
                1,
            )
            rotated = cv2.warpAffine(
                cursor,
                M,
                (cursor.shape[1], cursor.shape[0]),
            )
            channels = cv2.split(rotated)
            mask = np.array(channels[2]).astype(np.float32)
            mask[channels[2] == 0] = 0
            mask[channels[2] > 0] = 1
            transparent_mask = cv2.merge([mask, mask, mask])
            template = cv2.merge([channels[0], channels[1], channels[2]])
            matched = cv2.matchTemplate(img, template, (cv2.TM_CCORR_NORMED), mask=transparent_mask)
            if np.max(matched) > max_val:
                # if a better match was found then save the best match
                max_val = np.max(matched)
                rotation = i
                best_template = template
                best_trans_mask = transparent_mask
                best_match = matched
                boxx = cv2.minMaxLoc(matched)
        confidence, orientation, topleft = max_val, rotation, boxx[-1]
        if not minimap:
            # sets the player position extracted from the map
            self.x, self.y = (topleft[0] + width / 2, topleft[1] + height / 2)
        else:
            # sets the player orientation extracted from the minimap
            self.orientation = orientation

    def calc_angle(self, destination: tuple[int, int]):
        # calculates the angle between the player and the destination
        distance_m = np.sqrt((destination[0] - self.position[0]) ** 2 + (destination[1] - self.position[1]) ** 2)
        print(distance_m)
        anglef_origin = np.rad2deg(np.arcsin((self.position[0] - destination[0]) / distance_m))
        print("angle from origin", anglef_origin, "player angle", self.orientation)
        anglet_dest = self.orientation - anglef_origin
        if self.position[1] < destination[1]:
            # if the player is above the destination
            if self.position[0] < destination[0]:
                # if the player is to the left of the destination
                anglet_dest += 90
            else:
                # if the player is to the right of the destination
                anglet_dest -= 90
        retval = anglet_dest % 360
        if retval < 180:
            return retval
        else:
            return 180 - retval

    def move(self, destination: tuple[int, int]):
        # Moves the player to the specified direction
        distance = None, None
        calib = True
        key_pressed = False
        while distance != (0, 0):
            # gets the player orientation
            self.get_current_position()
            # gets the player position
            self.get_current_position(
                range(self.orientation - 10, self.orientation + 10, 5),
                minimap=False,
                map_loc=destination,
            )
            # calculates the distance vector
            distance = (
                destination[0] - self.position[0],
                destination[1] - self.position[1],
            )
            if (
                int(floor(distance[0] * 10) / 10),
                int(floor(distance[1] * 10) / 10),
            ) == (0, 0):
                # if the player is at the destination approximate to 10 pixels
                print("destination reached")
                return
            if key_pressed:
                # if a key was pressed then remove press
                key_pressed = False
                pyautogui.keyUp("w")
            prevangle = None
            prev_move = None
            while calib:
                x, y = autoit.mouse_get_pos()
                if x > 1900 or x < 100:
                    # if the mouse is out of the screen then move to middle of the screen
                    pyautogui.press("m")
                    autoit.mouse_move(960, y)  # DEV make dynamic
                    pyautogui.press("m")
                x, y = autoit.mouse_get_pos()
                angle_needed = self.calc_angle(destination)
                # move to the angle needed in the fastest direction
                pixel_distance = 250 * (angle_needed / abs(angle_needed))
                if prevangle is not None:
                    # if the angle difference is too large then don't change direction
                    # WARNING not working aslan might as well remove
                    diff = abs(angle_needed) + abs(prevangle)
                    if 20 <= diff <= 340:
                        prevangle = angle_needed
                        prev_move = pixel_distance
                    else:
                        print("angle difference too large, correcting")
                        pixel_distance = prev_move
                autoit.mouse_move(int(x) + int(pixel_distance), int(y))
                print("moved", pixel_distance)
                self.get_current_position()
                if 5 > abs(self.calc_angle(destination)):
                    calib = False
                if 5 > (180 + self.calc_angle(destination)):
                    calib = False
                print("need to turn", angle_needed)
            print("orientation calibration complete")

            # move player forward
            pyautogui.keyDown("w")
            key_pressed = True
            time.sleep(2.5)


if __name__ == "__main__":
    time.sleep(5)
    begin = time.time()
    player = Player("./icons/player_cursor.png")
    player.move((1580, 616))
    print("time: ", time.time() - begin)
