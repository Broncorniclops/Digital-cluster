import json
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.core.window import Window

LAYOUT_SAVE_PATH = "config/layout.json"

class DraggableWidget(DragBehavior, Widget):
    def __init__(self, wrapped_widget, widget_id, **kwargs):
        super().__init__(**kwargs)
        self.widget_id = widget_id
        self.add_widget(wrapped_widget)
        self.size_hint = (None, None)
        self.size = wrapped_widget.size
        self.drag_rectangle = (0, 0, self.width, self.height)
        self.drag_timeout = 10000000  # effectively always draggable
        self.drag_distance = 1

    def get_position_data(self):
        return {
            "id": self.widget_id,
            "x": self.x / Window.width,
            "y": self.y / Window.height
        }

    def set_position_data(self, data):
        self.pos = (data["x"] * Window.width, data["y"] * Window.height)


class DraggableLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.widgets = {}

    def add_draggable_widget(self, widget, widget_id):
        draggable = DraggableWidget(widget, widget_id)
        self.widgets[widget_id] = draggable
        self.add_widget(draggable)

    def save_layout(self):
        layout_data = [w.get_position_data() for w in self.widgets.values()]
        with open(LAYOUT_SAVE_PATH, "w") as f:
            json.dump(layout_data, f)

    def load_layout(self):
        try:
            with open(LAYOUT_SAVE_PATH, "r") as f:
                layout_data = json.load(f)
            for data in layout_data:
                widget_id = data["id"]
                if widget_id in self.widgets:
                    self.widgets[widget_id].set_position_data(data)
        except FileNotFoundError:
            print("Layout file not found. Using defaults.")
