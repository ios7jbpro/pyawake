import pystray
import pystray._win32 as win32
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import ctypes
from ctypes import wintypes
import sys
import threading
import time

# Constants for Windows API
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

class PowerToysAwake:
    def __init__(self):
        self.current_mode = 0  # 0: Default, 1: Screen off, 2: Screen on
        self.active = False
        self.icon = None
        self.setup_icon()
        
    def setup_icon(self):
        # Create a simple icon
        image = Image.new('RGB', (64, 64), (70, 130, 180))
        dc = ImageDraw.Draw(image)
        dc.ellipse((15, 15, 49, 49), fill=(255, 215, 0))
        dc.rectangle((28, 20, 36, 44), fill=(255, 215, 0))
        
        self.icon = pystray.Icon("PowerToysAwake", image, menu=pystray.Menu(
            item('Default', self.set_default),
            item('Keep awake (Screen off)', self.set_screen_off),
            item('Keep awake (Screen on)', self.set_screen_on),
            item('Exit', self.quit_app)
        ))
        
    def set_keep_awake(self, screen_on=False):
        flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED
        if screen_on:
            flags |= ES_DISPLAY_REQUIRED
            
        ctypes.windll.kernel32.SetThreadExecutionState(flags)
        
    def disable_keep_awake(self):
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        
    def set_default(self):
        self.current_mode = 0
        self.active = False
        self.disable_keep_awake()
        self.update_tooltip()
        
    def set_screen_off(self):
        self.current_mode = 1
        self.active = True
        self.set_keep_awake(screen_on=False)
        self.update_tooltip()
        
    def set_screen_on(self):
        self.current_mode = 2
        self.active = True
        self.set_keep_awake(screen_on=True)
        self.update_tooltip()
        
    def update_tooltip(self):
        tooltips = {
            0: "PowerToys Awake - Default",
            1: "PowerToys Awake - Keep awake (Screen off)",
            2: "PowerToys Awake - Keep awake (Screen on)"
        }
        self.icon.title = tooltips[self.current_mode]
        
    def quit_app(self):
        self.active = False
        self.disable_keep_awake()
        self.icon.stop()
        
    def run(self):
        self.update_tooltip()
        self.icon.run()

if __name__ == "__main__":
    app = PowerToysAwake()
    app.run()