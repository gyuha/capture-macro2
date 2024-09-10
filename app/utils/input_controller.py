from pynput import keyboard, mouse
from pynput.mouse import Button

from app.utils.pynput_keymap import get_key_from_string


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
        """
        click_mouse() clicks the left mouse button once.
        """
        self.mouse.click(Button.left, 1)

    def press_key(self, key):
        send_key = get_key_from_string(key)
        self.keyboard.press(send_key)
        self.keyboard.release(send_key)

    def scroll_mouse(self, clicks):
        self.mouse.scroll(0, clicks)

    def get_mouse_position(self):
        return self.mouse.position

        # Usage example:
# controller = InputController()
# controller.move_mouse(100, 100)
# controller.click_mouse()
# controller.press_key('a')
# controller.scroll_mouse(-1)  # Scroll down
