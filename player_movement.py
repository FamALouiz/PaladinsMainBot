import numpy as np, cv2, json, math, pyautogui, keyboard, time, datetime, win32gui, win32con, random
from PIL import ImageGrab


class PlayerMovement:
    def __init__(self, player_cursor_img):
        self.land_locations = [
            [524, 284],
            [513, 238],
            [571, 443],
            [583, 419],
            [610, 380],
            [678, 367],
            [734, 377],
            [727, 324],
            [749, 342],
            [524, 636],
            [516, 656],
            [513, 672],
            [553, 605],
            [523, 572],
            [482, 555],
            [668, 699],
            [504, 485],
            [486, 499],
            [492, 475],
            [256, 467],
            [152, 297],
            [392, 441],
            [406, 430],
            [413, 416],
            [451, 454],
            [425, 422],
            [428, 405],
            [526, 409],
            [531, 393],
            [498, 402],
            [577, 388],
            [595, 343],
            [644, 620],
            [636, 609],
            [648, 606],
            [645, 600],
            [659, 605],
            [692, 753],
            [676, 745],
            [681, 820],
            [679, 845],
            [759, 670],
            [790, 621],
            [775, 573],
            [769, 583],
            [750, 583],
            [748, 603],
            [761, 599],
            [692, 681],
            [760, 350],
            [908, 375],
            [873, 383],
            [892, 396],
            [893, 410],
            [889, 356],
            [534, 566],
            [535, 552],
            [405, 821],
            [417, 836],
            [427, 823],
            [451, 746],
            [439, 724],
            [583, 799],
            [563, 770],
            [508, 787],
            [515, 841],
            [651, 907],
            [592, 672],
            [683, 642],
            [634, 425],
            [614, 404],
            [605, 299],
            [657, 182],
            [562, 151],
            [650, 293],
            [612, 317],
            [311, 168],
            [318, 105],
            [299, 86],
            [358, 100],
            [457, 140],
            [497, 194],
            [424, 160],
            [437, 270],
            [468, 284],
            [434, 318],
            [403, 372],
            [422, 345],
            [636, 395],
            [892, 573],
            [908, 473],
            [930, 533],
            [997, 456],
            [960, 392],
            [989, 533],
            [959, 535],
            [484, 891],
            [514, 875],
            [481, 709],
            [373, 763],
        ]
        self.player_cursor_img = player_cursor_img

    def land_at_closest_loc(self):
        player_height, player_width, _ = self.player_cursor_img.shape
        player_orient_set = False
        rotation = 0
        startTimestamp = datetime.datetime.now().timestamp()
        while True:
            if datetime.datetime.now().timestamp() - startTimestamp > 90.0:
                pyautogui.press("m")
                pyautogui.press("space")
                keyboard.press("space")
                break
            try:
                handle = win32gui.GetForegroundWindow()
                bbox = win32gui.GetWindowRect(handle)
                screenshot = ImageGrab.grab(bbox)
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                map_img = self._extract_map(screenshot)
                map_height, map_width, _ = map_img.shape
                if not player_orient_set:
                    rotation, _, _, best_match = self.get_player_orient(
                        10,
                        [0, 360],
                        self.player_cursor_img,
                        player_width,
                        player_height,
                        map_img,
                    )
                    _, _, _, player_pos = cv2.minMaxLoc(best_match)
                    player_pos = (
                        player_pos[0] + player_width / 2,
                        player_pos[1] + player_height / 2,
                    )
                    map_region = map_img[
                        int(player_pos[1] - 30) : int(player_pos[1] + 30),
                        int(player_pos[0] - 30) : int(player_pos[0] + 30),
                    ]
                    (
                        rotation,
                        best_template,
                        best_trans_mask,
                        _,
                    ) = self.get_player_orient(
                        1,
                        [rotation - 8, rotation + 8],
                        self.player_cursor_img,
                        player_width,
                        player_height,
                        map_region,
                    )
                    _, _, _, player_pos = cv2.minMaxLoc(best_match)
                    player_pos = (
                        player_pos[0] + player_width / 2,
                        player_pos[1] + player_height / 2,
                    )
                    closest_tree, dist = self.find_closest_loc(
                        player_pos, self.land_locations
                    )
                    player_orient_set = True
                best_match = cv2.matchTemplate(
                    map_img, best_template, (cv2.TM_CCORR_NORMED), mask=best_trans_mask
                )
                _, _, _, player_pos = cv2.minMaxLoc(best_match)
                player_pos = (
                    player_pos[0] + player_width / 2,
                    player_pos[1] + player_height / 2,
                )
                move_vector = (
                    closest_tree[0] - player_pos[0],
                    player_pos[1] - closest_tree[1],
                )
                move_vector = self.rotate_point((0, 0), move_vector, -rotation)
                if move_vector[0] <= 0.8:
                    if move_vector[1] <= 0.8:
                        if move_vector[0] >= -0.8:
                            if move_vector[1] >= -0.8:
                                pyautogui.press("m")
                                pyautogui.press("space")
                                keyboard.press("space")
                                break
                self.move_player(map_height, move_vector)
            except:
                pyautogui.press("m")
                pyautogui.press("space")
                keyboard.press("space")
                break

    def move_player(self, map_height, move_vector):
        move_speed_ad = map_height / 1080 * 6.37
        move_speed_w = map_height / 1080 * 7.95
        move_speed_s = map_height / 1080 * 5.2
        keys = []
        if move_vector[0] > 0.8:
            keys.append("d")
        else:
            if move_vector[0] < -0.8:
                keys.append("a")
            if move_vector[1] > 0.8:
                keys.append("w")
            elif move_vector[1] < -0.8:
                keys.append("s")
        if len(keys) == 2:
            k = random.randint(0, 7)
            if k < 2:
                keys = [keys[k]]
        max_time = 10000
        for key in keys:
            if key == "d" or key == "a":
                curr_time = np.abs(move_vector[0]) / move_speed_ad
            else:
                if key == "w":
                    curr_time = np.abs(move_vector[1]) / move_speed_w
                else:
                    if key == "s":
                        curr_time = np.abs(move_vector[1]) / move_speed_s
            if curr_time < max_time:
                max_time = curr_time

        rand_time = random.random() * (max_time / 2) + max_time / 2
        self.hold_keys(keys, rand_time)

    @staticmethod
    def hold_keys(keys, hold_time):
        start = time.time()
        while time.time() - start < hold_time:
            for key in keys:
                pyautogui.keyDown(key)

        for key in keys:
            pyautogui.keyUp(key)

    @staticmethod
    def rotate_point(origin, point, angle, deg=True):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        if deg:
            angle = math.pi * angle / 180
        ox, oy = origin
        px, py = point
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return (qx, qy)

    def get_player_orient(
        self,
        step,
        range_min_max,
        player_cursor_img,
        player_width,
        player_height,
        map_img,
    ):
        max_val = 0
        rotation = 0
        best_match = []
        for i in range(range_min_max[0], range_min_max[1], step):
            M = cv2.getRotationMatrix2D(
                ((player_width - 1) / 2, (player_height - 1) / 2), i, 1
            )
            rotated = cv2.warpAffine(
                player_cursor_img, M, (player_width, player_height), borderValue=0
            )
            channels = cv2.split(rotated)
            mask = np.array(channels[3]).astype(np.float32)
            mask[channels[3] == 0] = 0
            mask[channels[3] > 0] = 1
            transparent_mask = cv2.merge([mask, mask, mask])
            template = cv2.merge([channels[0], channels[1], channels[2]])
            matched = cv2.matchTemplate(
                map_img, template, (cv2.TM_CCORR_NORMED), mask=transparent_mask
            )
            if np.max(matched) > max_val:
                max_val = np.max(matched)
                rotation = i
                best_template = template
                best_trans_mask = transparent_mask
                best_match = matched

        return (rotation, best_template, best_trans_mask, best_match)

    @staticmethod
    def _extract_map(img):
        height, width, _ = img.shape
        map = img[
            : height - 1,
            int((width - height) / 2) : int((width - height) / 2 + height - 1),
        ]
        return map

    @staticmethod
    def find_closest_loc(my_loc, loc_array):
        def distance(p1, p2):
            return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        min_dist = np.inf
        closest = None
        for tree in loc_array:
            dist = distance(my_loc, tree)
            if dist < min_dist:
                min_dist = dist
                closest = tree

        return (closest, min_dist)


if __name__ == "__main__":
    pass
