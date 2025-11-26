import configparser
from pathlib import Path

# Defaults
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

BLINK_RATE = 0.5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 70)
RED = (200, 30, 30)

TIMED_DURATION_SEC = 60
HUD_HEIGHT = 70
ALLOW_BACKSPACE = True


def _parse_color(value: str):
    parts = value.split(",")
    if len(parts) == 3:
        try:
            return tuple(int(p.strip()) for p in parts)
        except ValueError:
            return None
    if value.startswith("#") and len(value) in (7, 9):
        try:
            return tuple(int(value[i:i+2], 16) for i in (1, 3, 5))
        except ValueError:
            return None
    return None


def load_settings(path: str | Path = "settings.ini"):
    global SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLINK_RATE, WHITE, BLACK, GREEN, RED, TIMED_DURATION_SEC, HUD_HEIGHT, ALLOW_BACKSPACE
    ini_path = Path(path)
    if not ini_path.exists():
        return
    config = configparser.ConfigParser()
    config.read(ini_path)

    if "display" in config:
        SCREEN_WIDTH = config.getint("display", "width", fallback=SCREEN_WIDTH)
        SCREEN_HEIGHT = config.getint("display", "height", fallback=SCREEN_HEIGHT)
        FPS = config.getint("display", "fps", fallback=FPS)
        HUD_HEIGHT = config.getint("display", "hud_height", fallback=HUD_HEIGHT)

    if "timed" in config:
        TIMED_DURATION_SEC = config.getint("timed", "duration_sec", fallback=TIMED_DURATION_SEC)

    if "input" in config:
        ALLOW_BACKSPACE = config.getboolean("input", "allow_backspace", fallback=ALLOW_BACKSPACE)

    if "cursor" in config:
        BLINK_RATE = config.getfloat("cursor", "blink_rate", fallback=BLINK_RATE)

    if "colors" in config:
        for name in ("white", "black", "green", "red"):
            val = config["colors"].get(name)
            if val:
                parsed = _parse_color(val)
                if parsed:
                    if name == "white":
                        WHITE = parsed
                    elif name == "black":
                        BLACK = parsed
                    elif name == "green":
                        GREEN = parsed
                    elif name == "red":
                        RED = parsed


# Apply settings at import time so downstream modules see overrides.
load_settings()
