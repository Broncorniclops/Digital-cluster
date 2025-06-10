
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from layout_manager import list_profiles, load_layout, save_layout, set_default_profile, get_default_profile

class LayoutProfilePopup(Popup):
    def __init__(self, get_cb, apply_cb, **kwargs):
        super().__init__(**kwargs)
        self.title = "Layout Profiles"
        self.size_hint = (0.8, 0.8)
        self.get_cb = get_cb
        self.apply_cb = apply_cb
        self.selected_profile = None
        self.default_profile = get_default_profile()
        self.toggle_group = []

        self.layout = BoxLayout(orientation="vertical")
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.profile_list = BoxLayout(orientation="vertical", size_hint_y=None)
        self.profile_list.bind(minimum_height=self.profile_list.setter("height"))
        self.scroll.add_widget(self.profile_list)
        self.layout.add_widget(self.scroll)

        self.btn_bar = BoxLayout(size_hint=(1, 0.2))
        self.save_btn = Button(text="Save Current")
        self.save_btn.bind(on_release=self.save_current_layout)
        self.set_default_btn = Button(text="Set Default")
        self.set_default_btn.bind(on_release=self.set_default_profile)
        self.close_btn = Button(text="Close")
        self.close_btn.bind(on_release=self.dismiss)

        self.btn_bar.add_widget(self.save_btn)
        self.btn_bar.add_widget(self.set_default_btn)
        self.btn_bar.add_widget(self.close_btn)

        self.layout.add_widget(self.btn_bar)
        self.add_widget(self.layout)
        self.populate_profiles()

    def populate_profiles(self):
        self.profile_list.clear_widgets()
        self.toggle_group.clear()
        for name in list_profiles():
            row = BoxLayout(size_hint_y=None, height=40)
            toggle = ToggleButton(text=name,
                                  group="profile_select",
                                  state="down" if name == self.default_profile else "normal")
            toggle.bind(on_release=self.select_profile)
            self.toggle_group.append(toggle)
            load_btn = Button(text="Load", size_hint_x=0.3)
            load_btn.bind(on_release=lambda btn, name=name: self.load_selected(name))
            del_btn = Button(text="X", size_hint_x=0.2)
            del_btn.bind(on_release=lambda btn, name=name: self.delete_profile(name))
            row.add_widget(toggle)
            row.add_widget(load_btn)
            row.add_widget(del_btn)
            self.profile_list.add_widget(row)

    def select_profile(self, instance):
        self.selected_profile = instance.text

    def load_selected(self, name):
        layout = load_layout(name)
        self.apply_cb(layout)

    def delete_profile(self, name):
        import os
        os.remove(f"/home/pi/layout_profiles/{name}.json")
        self.populate_profiles()

    def save_current_layout(self, instance):
        from kivy.uix.textinput import TextInput
        popup = Popup(title="Save Layout As", size_hint=(0.6, 0.4))
        box = BoxLayout(orientation="vertical")
        text_input = TextInput(hint_text="Enter profile name")
        save_btn = Button(text="Save")
        save_btn.bind(on_release=lambda btn: self._do_save_profile(popup, text_input.text.strip()))
        box.add_widget(text_input)
        box.add_widget(save_btn)
        popup.content = box
        popup.open()

    def _do_save_profile(self, popup, name):
        if name:
            layout = self.get_cb()
            save_layout(name, layout)
            popup.dismiss()
            self.populate_profiles()

    def set_default_profile(self, instance):
        if self.selected_profile:
            set_default_profile(self.selected_profile)
            self.default_profile = self.selected_profile
            self.populate_profiles()
