import os

env = os.environ.get("ENV", "development").lower()

if env == "production":
    from .prod import *
else:
    from .dev import *


