from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.animation import Animation
import math

class CircularGauge(BoxLayout):
    value = NumericProperty(0)
    displayed_value = NumericProperty(0)
    max_value = NumericProperty(100)
    unit = StringProperty("")
    title = StringProperty("")
    redline_start = NumericProperty(None)
    ticks = ListProperty([])
    digital_only = BooleanProperty(False)
    faulted = BooleanProperty(False)  # <-- Fault detection support

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.value_label = Label(text='0', font_size=32)
        self.title_label = Label(text=self.title, font_size=20)
        self.canvas_widget = Widget(size_hint=(1, 1))

        self.add_widget(self.title_label)
        self.add_widget(self.canvas_widget)
        self.add_widget(self.value_label)

        self.flash_alpha = 0.0
        self.bind(displayed_value=self._update_display, size=self._draw_gauge, pos=self._draw_gauge)
        self.bind(faulted=self._draw_gauge)  # update overlay if fault state changes

    def _update_display(self, instance, value):
        self.value_label.text = f"{int(value)} {self.unit}"
        self._draw_gauge()

        if self.redline_start and self.value > self.redline_start:
            self._trigger_flash()

    def _trigger_flash(self):
        anim = Animation(flash_alpha=1.0, duration=0.1) + Animation(flash_alpha=0.0, duration=0.1)
        anim.start(self)

    def set_value(self, new_value, faulted=False):
        new_value = max(0, min(new_value, self.max_value))
        self.value = new_value
        self.faulted = faulted
        anim = Animation(displayed_value=new_value, duration=0.3, t='out_quad')
        anim.start(self)

    def _draw_gauge(self, *args):
        self.canvas_widget.canvas.clear()
        if self.digital_only:
            return

        with self.canvas_widget.canvas:
            center_x = self.canvas_widget.center_x
            center_y = self.canvas_widget.center_y
            radius = min(self.canvas_widget.width, self.canvas_widget.height) / 2.5
            start_angle = 135
            end_angle = 405
            sweep_angle = end_angle - start_angle

            # Gauge background ring
            Color(0.2, 0.2, 0.2)
            Line(circle=(center_x, center_y, radius), width=4)

            # Redline arc
            if self.redline_start and self.redline_start < self.max_value:
                red_start = start_angle + sweep_angle * (self.redline_start / self.max_value)
                red_end = end_angle
                Color(1, 0, 0)
                Line(circle=(center_x, center_y, radius, red_start, red_end), width=4)

            # Tick marks
            if self.ticks:
                Color(1, 1, 1)
                tick_length = radius * 0.1
                for tick in self.ticks:
                    angle = start_angle + sweep_angle * (tick / self.max_value)
                    rad = math.radians(angle)
                    x1 = center_x + (radius - tick_length) * math.cos(rad)
                    y1 = center_y + (radius - tick_length) * math.sin(rad)
                    x2 = center_x + radius * math.cos(rad)
                    y2 = center_y + radius * math.sin(rad)
                    Line(points=[x1, y1, x2, y2], width=1)

            # Needle
            Color(0.8, 0.8, 0)
            value_angle = start_angle + sweep_angle * (self.displayed_value / self.max_value)
            radians = math.radians(value_angle)
            needle_length = radius * 0.9
            x_end = center_x + needle_length * math.cos(radians)
            y_end = center_y + needle_length * math.sin(radians)
            Line(points=[center_x, center_y, x_end, y_end], width=3)

            # Flash overlay
            if self.flash_alpha > 0:
                Color(1, 0, 0, self.flash_alpha)
                Line(circle=(center_x, center_y, radius * 1.05), width=6)

            # Fault overlay icon
            if self.faulted:
                Color(1, 0.2, 0.2, 0.7)
                Rectangle(pos=(center_x - 20, center_y + radius + 5), size=(40, 40))
                Color(1, 1, 1, 1)
                Rectangle(pos=(center_x - 10, center_y + radius + 15), size=(20, 20))
