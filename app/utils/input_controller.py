
import platform
import time
import pyautogui

from app.utils.pynput_keymap import get_key_from_string


class InputController:
    def __init__(self):
        self.system = platform.system()
        if self.system == "Windows":
            from pynput import mouse, keyboard
            self.mouse = mouse.Controller()
            self.keyboard = keyboard.Controller()
        elif self.system == "Darwin":  # macOS
            pass  # We'll use pyautogui for macOS
        else:
            raise NotImplementedError(f"Unsupported operating system: {self.system}")

    def move_mouse(self, x, y):
        if self.system == "Windows":
            self.mouse.position = (x, y)
        elif self.system == "Darwin":
            pyautogui.moveTo(x, y)

    def click_mouse(self):
        if self.system == "Windows":
            self.mouse.click(self.mouse.Button.left)
        elif self.system == "Darwin":
            pyautogui.click()

    def press_key(self, key):
        if self.system == "Windows":
            send_key = get_key_from_string(key)
            self.keyboard.press(send_key)
            self.keyboard.release(send_key)
        elif self.system == "Darwin":
            pyautogui.press(key)

    def scroll_mouse(self, clicks):
        if self.system == "Windows":
            self.mouse.scroll(0, clicks)
        elif self.system == "Darwin":
            pyautogui.scroll(clicks)

    def get_mouse_position(self):
        if self.system == "Windows":
            pos = self.mouse.position
            return (pos.x, pos.y)  # Convert Point to tuple
        elif self.system == "Darwin":
            return pyautogui.position()  # Already returns a tuple-like object

        # Usage example:
# controller = InputController()
# controller.move_mouse(100, 100)
# controller.click_mouse()
# controller.press_key('a')
# controller.scroll_mouse(-1)  # Scroll down
