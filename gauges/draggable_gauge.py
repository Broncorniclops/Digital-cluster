
from kivy.uix.label import Label
from kivy.uix.behaviors import DragBehavior
from kivy.properties import StringProperty
from kivy.graphics import Color, Rectangle

class DraggableGauge(DragBehavior, Label):
    gauge_type = StringProperty("generic")

    def __init__(self, gauge_id, gauge_type="generic", **kwargs):
        super().__init__(**kwargs)
        self.id = gauge_id
        self.gauge_type = gauge_type
        self.size_hint = kwargs.get("size_hint", (0.2, 0.2))
        self.pos_hint = kwargs.get("pos_hint", {"x": 0.4, "y": 0.4})
        self.text = f"{gauge_type.upper()}"
        self.font_size = 20
        self.bold = True
        self.halign = "center"
        self.valign = "middle"
        self.color = (1, 1, 1, 1)
        self.markup = True

        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 0.6)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def update_visuals(self):
        # Placeholder for updating visuals
        pass
