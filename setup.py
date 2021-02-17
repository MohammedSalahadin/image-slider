
from distutils.core import setup
import py2exe

setup( windows = [{
            "script": "3-v3.py",
            "icon_resources": [(1, "app.ico")]
        }],)
