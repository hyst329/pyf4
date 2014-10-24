from distutils.core import setup
import os
import py2exe
from f4main import version

setup(
    console=["f4main.py"],
    zipfile=None,
    options={
        "py2exe": {
            "bundle_files": 1
        }
    }
)

outfile = "dist/f4main-%d.%d.%d.exe" % \
          (version["major"], version["minor"], version["patch"])
if os.path.exists(outfile):
    os.remove(outfile)
os.rename("dist/f4main.exe",
          outfile)
os.system("upx -9 %s" % outfile)