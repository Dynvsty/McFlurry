# ©2023 by Insomnix Inc.

import win32api
import win32gui
import win32con
import keyboard
import os
import sys
import mouse
from PIL import Image
import pystray
import signal
import threading

#global hotkey

def fix_hotkey(hotkey):
    keyboard.add_hotkey(hotkey, lambda: on_hotkey_pressed() if mouse.is_pressed(button='left') else None)
    keyboard.add_hotkey(hotkey, lambda: on_hotkey_pressed() if mouse.is_pressed(button='right') else None)

if getattr(sys, 'frozen', False):
    # We are running in a bundle
    bundle_dir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.abspath(os.path.dirname(__file__))

# Use bundle_dir to locate the icon file
icon_path = os.path.join(bundle_dir, "assets/icon.ico")


# Simulate right clicking on the window bar
def simulate_window_right_click(title):
    hwnd = None
    # Get the minecraft program id
    def callback(handle, data):
        nonlocal hwnd
        window_title = win32gui.GetWindowText(handle).lower()
        if window_title.startswith(title.lower()) and window_title != "minecraft launcher" and window_title != "minecraft game output":
            hwnd = handle


    win32gui.EnumWindows(callback, None)
    if hwnd is None:
        print(f"Could not find window with title '{title}'")
        return
    
    style = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)

    # If window is fullscreened, un-fullscreen & click the title bar
    if not (style & win32con.WS_OVERLAPPEDWINDOW):
        win32api.SetWindowLong(hwnd, win32con.GWL_STYLE,
                               win32con.WS_OVERLAPPEDWINDOW)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)
        x, y = 0, 0  # Coordinates of the right-click relative to the top-left corner of the window
        win32api.SendMessage(hwnd, win32con.WM_NCRBUTTONDOWN, win32con.HTCAPTION, win32api.MAKELONG(x, y))
        win32api.SendMessage(hwnd, win32con.WM_NCRBUTTONUP, win32con.HTCAPTION, win32api.MAKELONG(x, y))
        # Re-Fullscreen the window
        win32api.SetWindowLong(hwnd, win32con.GWL_STYLE,
                               win32con.WS_POPUP | win32con.WS_VISIBLE)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)

    # If window is not fullscreened, click the title bar
    else:
        x, y = 0, 0  # Coordinates of the right-click relative to the top-left corner of the window
        win32api.SendMessage(hwnd, win32con.WM_NCRBUTTONDOWN, win32con.HTCAPTION, win32api.MAKELONG(x, y))
        win32api.SendMessage(hwnd, win32con.WM_NCRBUTTONUP, win32con.HTCAPTION, win32api.MAKELONG(x, y))


def on_hotkey_pressed():
    simulate_window_right_click("Minecraft")

# Define the message box title and messages
title = "McFlurry"
message = "Would you like to create a custom keybind?\nIf so, press Ok.\nOtherwise press Cancel to use the default (ctrl+alt+x)."
recording_message = "After you press OK, recording will start.\nPress the keys you would like as your keybind, then press ESC"

# Show the message box with "OK" and "Cancel" buttons
response = win32api.MessageBox(None, message, title, win32con.MB_OKCANCEL)

def record_hotkey():
    # Record keyboard events until 'esc' key is pressed
    events = keyboard.record(until='esc')

    # Filter key down events and get their names
    key_down_events = [event.name for event in events if event.event_type == keyboard.KEY_DOWN]

    # Get the hotkey name from the key down events
    hotkey = keyboard.get_hotkey_name(key_down_events)
    hotkey = hotkey.replace("esc+", "")
    hotkey = hotkey.replace("esc", "")
    

    # Make sure the hotkey is not empty
    if len(hotkey) <= 0:
        message = f'Please choose a longer hotkey.\nPress OK to record again.'
        win32api.MessageBox(None, message, title, win32con.MB_OK)
        return record_hotkey()
    else:
        pass

    # Register the hotkeys
    done_message = f'Your keybind "{hotkey}", has been recorded.\nPress OK to continue'
    
    # Register the keyboard hotkey
    keyboard.add_hotkey(hotkey, on_hotkey_pressed)
    fix_hotkey(hotkey)
    win32api.MessageBox(None, done_message, title, win32con.MB_OK)

# Check which button was clicked
if response == win32con.IDOK:
    win32api.MessageBox(None, recording_message, title, win32con.MB_OK)
    record_hotkey()
else:
    hotkey = 'ctrl+alt+x'
    fix_hotkey(hotkey)
    keyboard.add_hotkey(hotkey, on_hotkey_pressed)

def on_quit():
    icon.stop()
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)

# Create the system tray icon
image = Image.open(icon_path)
menu = pystray.Menu(pystray.MenuItem("Quit", on_quit))
icon = pystray.Icon("mcflurry", image, "McFlurry", menu)
icon.run()
