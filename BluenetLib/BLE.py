from BluenetLib.lib.core.BluetoothCore import BluetoothCore

class BluenetBle(BluetoothCore):
    """
    This is a wrapper class to expose an API through the BluenetLib package.
    """
    
    def __init__(self):
        super().__init__()
