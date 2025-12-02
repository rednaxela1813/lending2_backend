import logging
from typing import Dict, List

from django.conf import settings


def get_logging_config(debug: bool = False) -> Dict:
    """
    Build a LOGGING dict that:
    - Logs to console for all environments.
    - Sends error/critical logs to ADMINS via email when DEBUG is False and ADMINS is set.
    """
    has_admins = bool(getattr(settings, "ADMINS", []))
    handlers: Dict[str, Dict] = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    }

    mail_handlers: List[str] = []
    if has_admins and not debug:
        handlers["mail_admins"] = {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        }
        mail_handlers.append("mail_admins")

    root_handlers = ["console"] + mail_handlers

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            },
        },
        "formatters": {
            "simple": {
                "format": "%(levelname)s %(name)s: %(message)s",
            },
        },
        "handlers": handlers,
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "django.request": {
                "handlers": root_handlers,
                "level": "ERROR",
                "propagate": False,
            },
            "django.server": {
                "handlers": root_handlers,
                "level": "ERROR",
                "propagate": False,
            },
            "apps": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": True,
            },
        },
        "root": {
            "handlers": root_handlers,
            "level": "INFO",
        },
    }

