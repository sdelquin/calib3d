from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).resolve().parent
PROJECT_NAME = PROJECT_DIR.name

CONFIG_FILE = config('CONFIG_FILE', default=PROJECT_DIR / 'config.yml', cast=Path)
AXIS_COLORS = {'X': 'red', 'Y': 'green', 'Z': 'blue'}

HISTORY_FILE = config('HISTORY_FILE', default=PROJECT_DIR / 'history.csv', cast=Path)
