import sys
from cx_Freeze import setup, Executable
from f4ver import verstrs

setup(name="pyf4helen",
      version=verstrs,
      description="Python implementation of the F4/Helen programming language",
      options={
          "build_exe": {
              "init_script": "Console",
              "include_files": ['library/'],
              "create_shared_zip": False
          },
          "bdist_msi": {
              "add_to_path": False
          }
      },
      executables=[Executable("f4main.py")],
      requires=['cx_Freeze', 'ply', 'termcolor'])