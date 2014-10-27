from distutils.core import setup
from Cython.Build import cythonize
from f4main import version

setup(
    name="PyF4",
    version="%d.%d.%d" % (version["major"], version["minor"], version["patch"]),
    ext_modules=cythonize("f4*.py"), requires=['Cython']
)