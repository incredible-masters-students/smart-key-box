import configparser
from pathlib import Path


PROJ_DIR = Path(__file__).parent.parent
SETTINGS_FILENAME = PROJ_DIR / "settings.cfg"

SMART_KEY_BOX_SETTINGS = configparser.ConfigParser()
SMART_KEY_BOX_SETTINGS.sections()
SMART_KEY_BOX_SETTINGS.read(SETTINGS_FILENAME)
