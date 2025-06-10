
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from gauge_screen import GaugeScreen
from settings_panel import SettingsPanel

class RootLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gauge_screen = GaugeScreen()
        self.add_widget(self.gauge_screen)

        self.settings_btn = Button(text="⚙️", size_hint=(0.1, 0.1), pos_hint={"right": 1.0, "top": 1.0})
        self.settings_btn.bind(on_release=self.toggle_settings)
        self.add_widget(self.settings_btn)

        self.settings_panel = SettingsPanel(gauge_screen_ref=self.gauge_screen, size_hint=(0.4, 0.8),
                                            pos_hint={"x": 0.6, "y": 0.1})
        self.settings_panel.opacity = 0
        self.settings_panel.disabled = True
        self.add_widget(self.settings_panel)

    def toggle_settings(self, instance):
        if self.settings_panel.opacity == 0:
            self.settings_panel.opacity = 1
            self.settings_panel.disabled = False
        else:
            self.settings_panel.opacity = 0
            self.settings_panel.disabled = True

class ClusterApp(App):
    def build(self):
        return RootLayout()

if __name__ == '__main__':
    ClusterApp().run()
