from distutils.core import setup
import py2exe

setup(
    console=["f4main.py"],
    zipfile=None,
    options={
        "py2exe": {
            "bundle_files": 1
        }
    }
)
