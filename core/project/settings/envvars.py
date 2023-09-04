from core.shared.utils.collections import deep_update
from core.shared.utils.settings import get_settings_from_env

# globals() is a dictionary of all global variables
deep_update(globals(),
            get_settings_from_env(ENV_PREFIX))  # type: ignore # noqa: F821
