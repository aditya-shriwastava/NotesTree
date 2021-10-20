#!/usr/bin/python3
import os

home = os.path.expanduser("~")
notestree = home + "/.local/bin/notestree"

if os.path.exists(notestree):
    os.system(f"rm {notestree}")
    print("Successfully Uninstalled!")
else:
    print("Already Uninstalled!")
