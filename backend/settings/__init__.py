import os


def _get_env_name():
    env = os.environ.get("ENV")
    if env:
        return env.lower()
    if "PYTEST_CURRENT_TEST" in os.environ:
        return "test"
    return "development"


env = _get_env_name()

if env == "production":
    from .prod import *
elif env == "test":
    from .test import *
else:
    from .dev import *

