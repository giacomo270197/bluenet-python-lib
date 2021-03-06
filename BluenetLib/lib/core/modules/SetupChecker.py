from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.topics.SystemBleTopics import SystemBleTopics


class SetupChecker:
    
    
    def __init__(self, address):
        self.address = address
        self.result = False
        
    def handleAdvertisement(self, advertisement):
        if "serviceData" not in advertisement:
            return
        
        if advertisement["address"] != self.address:
            return
        
        self.result = advertisement["serviceData"]["setupMode"]
    
    def getResult(self):
        return self.result