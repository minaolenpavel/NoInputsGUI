import noinputs

class DeviceManager:
    def __init__(self):
        self.devices:list = self.load_devices()

    def load_devices(self):
        devices = noinputs.list_devices()
        return devices