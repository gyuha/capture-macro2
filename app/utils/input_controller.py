import random
import time

from pynput import keyboard, mouse
from pynput.mouse import Button

from app.utils.pynput_keymap import get_key_from_string
from app.config.config import Config


class InputController:
    def __init__(self):
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()

    def move_mouse(self, x, y):
        """
        move_mouse(x, y) moves the mouse to the specified x, y coordinates.
        """
        self.mouse.position = (x, y)

    def click_mouse(self):
        cfg = Config()
        self.mouse.press(Button.left)
        time.sleep(random.randint(min(cfg.click_press_min, cfg.click_press_max),
                                  max(cfg.click_press_min, cfg.click_press_max)) / 1000)
        self.mouse.release(Button.left)

    def press_key(self, key):
        cfg = Config()
        send_key = get_key_from_string(key)
        if send_key is None:
            print(f"Unknown key: {key}")
            return
        self.keyboard.press(send_key)
        time.sleep(random.randint(min(cfg.key_press_min, cfg.key_press_max),
                                  max(cfg.key_press_min, cfg.key_press_max)) / 1000)
        self.keyboard.release(send_key)

    def scroll_mouse(self, clicks):
        self.mouse.scroll(0, clicks)

    def get_mouse_position(self):
        return self.mouse.position

    def swipe_mouse(self, start, end, duration=1.0):
        """
        Swipe the mouse from start to end in the given direction over the specified duration.
        :param start: Tuple (x, y) representing the start position
        :param end: Tuple (x, y) representing the end position
        :param duration: Duration of the swipe in seconds
        """
        self.mouse.position = start
        self.mouse.press(Button.left)

        steps = 100
        sleep_time = duration / steps
        x_step = (end[0] - start[0]) / steps
        new_x = start[0]

        for _ in range(steps):
            new_x = new_x + x_step
            self.mouse.position = (new_x, start[1])
            time.sleep(sleep_time)

        self.mouse.release(Button.left)


# controller = InputController()
# controller.move_mouse(100, 100)
# controller.click_mouse()
# controller.press_key('a')
# controller.scroll_mouse(-1)  # Scroll down
# controller.scroll_mouse(-1)  # Scroll down
