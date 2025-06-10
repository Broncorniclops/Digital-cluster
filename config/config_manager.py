
# config_manager.py

debug_enabled = True

def set_debug(enabled: bool):
    global debug_enabled
    debug_enabled = enabled

def is_debug():
    return debug_enabled
