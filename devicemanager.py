import noinputs
import subprocess
import re
import os
import sys

class DeviceManager:
    """
    Manager class to interact with the backend from the UI
    """
    def __init__(self):
        self.devices:list = self.load_devices()
        self.app_dir = os.environ.get("APPDIR", os.path.dirname(os.path.abspath(__file__)))

    def load_devices(self):
        devices = noinputs.list_devices()
        return devices
    
    def inhibit_device(self, index:int):
        device = self.devices[index]
        if device is not None:
            subprocess.run([
                "pkexec",
                sys.executable, # Point to the app image python interpreter
                os.path.join(self.app_dir, "noinputs.py"),
                "-i",
                re.findall(r'[1-9]', device.id)[0]
            ])

    def uninhibit_device(self, index:int):
        device = self.devices[index]
        if device is not None:
            subprocess.run([
                "pkexec",
                sys.executable,
                os.path.join(self.app_dir, "noinputs.py"),
                "-u",
                re.findall(r'[1-9]', device.id)[0]
            ])
