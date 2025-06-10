from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

class BarGauge(BoxLayout):
    value = NumericProperty(0)
    max_value = NumericProperty(100)
    unit = StringProperty("")
    title = StringProperty("")
    faulted = BooleanProperty(False)
    fault_message = StringProperty("Sensor fault")

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.label = Label(text=f"{self.title}", font_size=20)
        self.progress = ProgressBar(max=self.max_value, value=0)
        self.value_label = Label(text="0", font_size=16)
        self.overlay = Widget(size_hint=(1, 1))
        self.add_widget(self.label)
        self.add_widget(self.progress)
        self.add_widget(self.value_label)
        self.add_widget(self.overlay)

        self.bind(value=self._update)
        self.bind(faulted=self._draw_fault_overlay)

        self.overlay.bind(on_touch_down=self._on_touch)

    def _update(self, instance, val):
        self.progress.value = val
        self.value_label.text = f"{val:.1f} {self.unit}"
        self._draw_fault_overlay()

    def set_value(self, val, faulted=False, message="Sensor fault"):
        self.value = max(0, min(val, self.max_value))
        self.faulted = faulted
        self.fault_message = message

    def _draw_fault_overlay(self, *args):
        self.overlay.canvas.clear()
        if self.faulted:
            with self.overlay.canvas:
                Color(1, 0.2, 0.2, 0.6)
                Rectangle(pos=self.progress.pos, size=self.progress.size)

    def _on_touch(self, instance, touch):
        if self.faulted and self.collide_point(*touch.pos):
            popup = Popup(title=f"{self.title} Fault",
                          content=Label(text=self.fault_message),
                          size_hint=(None, None), size=(300, 200))
            popup.open()
            return True
        return False
