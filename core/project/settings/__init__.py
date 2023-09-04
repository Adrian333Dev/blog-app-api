import os.path
from pathlib import Path

from split_settings.tools import include, optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Namespaceing custom environment variables.
ENV_PREFIX = "DJAPP_"  # e.g. DJAPP_DEBUG
LOCAL_SETTINGS_PATH = os.getenv(f"{ENV_PREFIX}LOCAL_SETTINGS_PATH", None)

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = "local/settings.dev.py"

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

# Include settings:
include(
    "base.py",
    "custom.py",
    optional(LOCAL_SETTINGS_PATH),
    "envvars.py",
    "docker.py",
)
