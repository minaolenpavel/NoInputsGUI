import noinputs

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
            device.set_inhibit(True)

    def uninhibit_device(self, index:int):
        device = self.devices[index]
        if device is not None:
            device.set_inhibit(False)
