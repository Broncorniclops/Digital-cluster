from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock

class SplashScreen(FloatLayout):
    def __init__(self, proceed_callback, **kwargs):
        super().__init__(**kwargs)
        self.proceed_callback = proceed_callback

        # Logo at the top center (expects 'logo.png' in working directory)
        self.logo = Image(source="logo.png",
                          size_hint=(0.4, 0.4),
                          pos_hint={'center_x': 0.5, 'top': 0.95},
                          allow_stretch=True,
                          keep_ratio=True)
        self.add_widget(self.logo)

        # Status label at center
        self.status_label = Label(text="Initializing...",
                                  font_size=24,
                                  pos_hint={'center_x': 0.5, 'center_y': 0.3})
        self.add_widget(self.status_label)

        self.status_steps = [
            "⚙️ Initializing sensors...",
            "🔌 Checking UPS status...",
            "🌡️ Loading temperature controls...",
            "🧭 Launching gauge interface..."
        ]
        self.step = 0
        Clock.schedule_interval(self.next_step, 1)

    def next_step(self, dt):
        if self.step < len(self.status_steps):
            self.status_label.text = self.status_steps[self.step]
            self.step += 1
        else:
            Clock.unschedule(self.next_step)
            self.proceed_callback()
