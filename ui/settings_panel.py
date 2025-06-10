from font_selector_popup import FontSelectorPopup

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from config_manager import config_manager
from layout_profile_popup import LayoutProfilePopup
from log_cleanup_panel import LogCleanupPopup
from pid_mapping_popup import PIDMappingPopup
from dtc_viewer_panel import DTCViewerPopup
from gauge_manager_popup import GaugeManagerPopup

class SettingsPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.add_widget(ToggleButton(text='Night Mode',
                                     state='down' if config_manager.get("night_mode") else 'normal',
                                     on_press=self.toggle_night_mode))

        self.add_widget(ToggleButton(text='Diagnostic Overlay',
                                     state='down' if config_manager.get("diagnostic_overlay") else 'normal',
                                     on_press=self.toggle_diagnostics))

        self.add_widget(ToggleButton(text='Layout Edit Mode',
                                     state='down' if config_manager.get("layout_edit_mode") else 'normal',
                                     on_press=self.toggle_layout_edit))

        self.add_widget(ToggleButton(text='Auto Update Check',
                                     state='down' if config_manager.get("auto_update") else 'normal',
                                     on_press=self.toggle_update))

        self.add_widget(ToggleButton(text='Debug Logging',
                                     state='down' if config_manager.get("debug_logging") else 'normal',
                                     on_press=self.toggle_debug))

        self.add_widget(Button(text="Manage Layout Profiles", on_press=self.open_layout_profiles))
        self.add_widget(Button(text="Clean Up Logs", on_press=self.open_log_cleanup))
        self.add_widget(Button(text="Manage PID Mappings", on_press=self.open_pid_mappings))
        self.add_widget(Button(text="Open DTC Viewer", on_press=self.open_dtc_viewer))
        self.add_widget(Button(text="Manage Gauges", on_press=self.open_gauge_manager))

    def toggle_night_mode(self, btn):
        config_manager.set("night_mode", btn.state == 'down')

    def toggle_diagnostics(self, btn):
        config_manager.set("diagnostic_overlay", btn.state == 'down')

    def toggle_layout_edit(self, btn):
        config_manager.set("layout_edit_mode", btn.state == 'down')

    def toggle_update(self, btn):
        config_manager.set("auto_update", btn.state == 'down')

    def toggle_debug(self, btn):
        config_manager.set("debug_logging", btn.state == 'down')

    def open_layout_profiles(self, instance):
        popup = LayoutProfilePopup()
        popup.open()

    def open_log_cleanup(self, instance):
        popup = LogCleanupPopup()
        popup.open()

    def open_pid_mappings(self, instance):
        popup = PIDMappingPopup()
        popup.open()

    def open_dtc_viewer(self, instance):
        popup = DTCViewerPopup()
        popup.open()

    def open_gauge_manager(self, instance):
        popup = GaugeManagerPopup()
        popup.open()


    def open_gauge_manager(self):
        popup = GaugeManagerPopup()
        popup.open()
        

    def open_font_selector(self, instance):
        popup = FontSelectorPopup()
        popup.open()
