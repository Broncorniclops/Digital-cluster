# gesture_manager.py
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from time import time

class GestureManager:
    def __init__(self, gesture_callback):
        self.gesture_callback = gesture_callback
        self._touches = []
        self._start_time = None
        Window.bind(on_touch_down=self.on_touch_down, on_touch_up=self.on_touch_up)

    def on_touch_down(self, window, touch):
        self._touches.append(touch)
        if len(self._touches) == 1:
            self._start_time = time()
        return False

    def on_touch_up(self, window, touch):
        if touch in self._touches:
            self._touches.remove(touch)
        if len(self._touches) == 0 and self._start_time:
            duration = time() - self._start_time
            if duration < 0.3:
                self.gesture_callback("double_tap", touch)
            elif duration >= 1.0:
                self.gesture_callback("long_press", touch)
            self._start_time = None
        elif len(self._touches) == 2:
            self.gesture_callback("two_finger_swipe", touch)
        return False
