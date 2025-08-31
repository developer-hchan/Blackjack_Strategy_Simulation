from pathlib import Path
import tomllib

# global dictionaries used for caching
global_data_dictionary: dict[tuple, float] = {}
global_split_dictionary: dict[tuple, float] = {}

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# loading setting.toml
with open(BASE_DIR / "settings.toml", "rb") as f:
    global_config = tomllib.load(f)
