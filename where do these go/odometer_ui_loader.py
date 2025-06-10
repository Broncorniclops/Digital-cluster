
from ui.gauges.odometer_ui_overlay import OdometerOverlay

def load_odometer_overlay(screen):
    overlay = OdometerOverlay()
    screen.add_widget(overlay)
    return overlay
