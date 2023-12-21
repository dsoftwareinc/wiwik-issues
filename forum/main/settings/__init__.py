from .allauth import *
from .base import *
from .forum import *
from .installed_apps import *
from .logging import *
from .rq_queues import *
from .slack import *
from .static_files import *

DEBUG_TOOLS = False

if DEBUG_TOOLS:
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE
    INSTALLED_APPS.append("debug_toolbar")
