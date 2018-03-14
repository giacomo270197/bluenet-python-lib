from BluenetLib.lib.packets.ServiceData import ServiceData
from BluenetLib.lib.protocol.Services import DFU_ADVERTISEMENT_SERVICE_UUID
from BluenetLib.lib.util.Conversion import Conversion

import json

class Advertisement:
    name = ""
    address = None
    serviceUUID = None
    serviceData = None
    deviceType = None
    operationMode = None
    rssi = None
    
    def __init__(self, address, rssi, nameText, serviceDataText):
        self.address = address
        self.rssi = rssi
        self.name = nameText

        dataString = serviceDataText
        
        if serviceDataText is not None:
            dataArray = Conversion.hex_string_to_uint8_array(dataString)
            self.serviceUUID = Conversion.uint8_array_to_uint16([dataArray[0], dataArray[1]])

            # pop the service UUID
            dataArray.pop(0)
            dataArray.pop(0)
            
            if serviceDataText:
                self.serviceData = ServiceData(dataArray)
    
            self.operationMode = "NORMAL"

    
    def isInDFUMode(self):
        return self.operationMode == "DFU"
    
    def isInSetupMode(self):
        return self.operationMode == "SETUP"
    
    def isCrownstoneFamily(self):
        return self.serviceUUID == 0xC001 or self.serviceUUID == 0xC002 or self.serviceUUID == 0xC003 or self.serviceUUID == DFU_ADVERTISEMENT_SERVICE_UUID

    def hasScanResponse(self):
        return self.serviceData is not None
    
    def decrypt(self, key):
        if self.serviceData:
            self.serviceData.decrypt(key)
            
    def getDictionary(self):
        data = {}
    
        data["name"] = self.name
        data["rssi "] = self.rssi
        data["address"] = self.address
        data["serviceUUID"] = self.serviceUUID
        data["serviceData"] = self.serviceData.getDictionary()
    
        return data
    
