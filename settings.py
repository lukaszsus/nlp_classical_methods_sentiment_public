import os

PATH_TO_DATA = None
PROJECT_PATH = os.path.dirname(__file__)

try:
    from user_settings import *  # silence pyflakes
except ImportError:
    pass
