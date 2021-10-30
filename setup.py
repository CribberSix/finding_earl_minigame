import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

target = Executable(
    script="Adventure.py",
    base="Win32GUI",
    icon="ressources/bear.ico"
    )

setup(
    name="Finding earl",
    version="1.0",
    description="A text-based adventure game",
    options={"build_exe": build_exe_options},
    executables=[target]
)