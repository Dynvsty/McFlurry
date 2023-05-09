import win32api
import win32gui
import win32con
import keyboard
import os
import sys
from PIL import Image
import pystray
import signal
import threading

print("Running")

if getattr(sys, 'frozen', False):
    # we are running in a bundle
    bundle_dir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.abspath(os.path.dirname(__file__))

# use bundle_dir to locate the icon file
icon_path = os.path.join(bundle_dir, "assets/icon.ico")




def simulate_window_right_click(title):
    hwnd = None

    def callback(handle, data):
        nonlocal hwnd
        window_title = win32gui.GetWindowText(handle).lower()
        if window_title.startswith(title.lower()):
            if window_title != "minecraft game output":
                hwnd = handle

    win32gui.EnumWindows(callback, None)
    if hwnd is None:
        print(f"Could not find window with title '{title}'")
        return

    x, y = 0, 0  # Coordinates of the right-click relative to the top-left corner of the window
    win32api.SendMessage(hwnd, win32con.WM_NCRBUTTONDOWN, win32con.HTCAPTION, win32api.MAKELONG(x, y))
    win32api.SendMessage(hwnd, win32con.WM_NCRBUTTONUP, win32con.HTCAPTION, win32api.MAKELONG(x, y))


def on_hotkey_pressed():
    simulate_window_right_click("Minecraft")

keyboard.add_hotkey('ctrl+alt+x', on_hotkey_pressed)

hotkey_thread = threading.Thread(target=keyboard.wait)
hotkey_thread.daemon = True
hotkey_thread.start()


def on_quit():
    icon.stop()
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)

image = Image.open(icon_path)
menu = pystray.Menu(pystray.MenuItem("Quit", on_quit))
icon = pystray.Icon("mcflurry", image, "McFlurry", menu)

icon.run()