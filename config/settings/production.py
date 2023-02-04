import platform
from .base import *

# while we are locally testing any random string can do as the SECRET KEY
SECRET_KEY = get_env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
