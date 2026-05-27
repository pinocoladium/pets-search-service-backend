# flake8: noqa E401

from .settings import *  # noqa: F403


try:
    from .local_settings import *  # noqa: F403
except ImportError:
    pass
