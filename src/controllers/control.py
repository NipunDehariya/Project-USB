import subprocess
import os
import ctypes
import sys

# Path to the batch files
# block_path = "block_usb.bat"
# unblock_path = "unblock_usb.bat"

block_path = os.path.join(os.path.dirname(__file__), "block_usb.bat_Shortcut.lnk")
unblock_path = os.path.join(os.path.dirname(__file__), "unblock_usb.bat_Shortcut.lnk")


def run_as_admin(batch_file_path):
    os.startfile (batch_file_path)

def block():
    try:
        run_as_admin(block_path)
    except Exception as e:
        print("Error", str(e))

def unblock():
    try:
        run_as_admin(unblock_path)
    except Exception as e:
        print("Error", str(e))
        