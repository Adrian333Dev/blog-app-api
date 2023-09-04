from core.shared.utils.collections import deep_update
from core.shared.utils.settings import get_settings_from_env

"""
This takes the environment variables with the matching prefix, strips the prefix, and converts them to a dictionary.
And then it adds them to the global settings.

For example:
export DJAPP_IN_DOCKER=true (envorinment variable)

Could then be referenced as a global setting:
IN_DOCKER = True
"""

# globals() is a dictionary of all global variables
deep_update(globals(), get_settings_from_env(ENV_PREFIX)) # noqa # type: ignore
