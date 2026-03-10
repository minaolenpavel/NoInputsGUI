import noinputs
import subprocess
import re

class DeviceManager:
    """
    Manager class to interact with the backend from the UI
    """
    def __init__(self):
        self.devices:list = self.load_devices()

    def load_devices(self):
        devices = noinputs.list_devices()
        return devices
    
    def inhibit_device(self, index:int):
        device = self.devices[index]
        if device is not None:
            subprocess.run([
                "pkexec",
                "/usr/bin/noinputs",
                "-i",
                re.findall(r'[1-9]', device.id)[0]
            ])

    def uninhibit_device(self, index:int):
        device = self.devices[index]
        if device is not None:
            subprocess.run([
                "pkexec",
                "/usr/bin/noinputs",
                "-u",
                re.findall(r'[1-9]', device.id)[0]
            ])
