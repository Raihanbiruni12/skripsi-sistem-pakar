import json
import os

SETTINGS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'settings.json')

DEFAULT_SETTINGS = {
    "nama_sistem": "Sistem Pakar Diagnosa Penyakit Kulit",
    "email_admin": "admin@pakarkulit.com",
    "dark_mode": False,
    "maintenance_mode": False
}

def get_settings():
    if not os.path.exists(SETTINGS_PATH):
        # Create default if not exists
        with open(SETTINGS_PATH, 'w') as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)
        return DEFAULT_SETTINGS
        
    try:
        with open(SETTINGS_PATH, 'r') as f:
            return json.load(f)
    except Exception:
        return DEFAULT_SETTINGS

def save_settings(new_settings):
    settings = get_settings()
    settings.update(new_settings)
    
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    return settings
