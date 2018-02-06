from BluenetLib.lib.util.Conversion import Conversion

SERVICE_DATA_SIZE = 17

class ServiceDataPacket:
    opCode = 0
    dataType = 0
    crownstoneId = 0
    switchState = 0
    flagBitmask = 0
    temperature = 0
    powerFactor = 0
    powerUsageReal = 0
    energyUsed = 0
    partialTimestamp = 0
    validation = 0
    
    def __init__(self, payload):
        if len(payload) != SERVICE_DATA_SIZE:
            print("ERROR: INVALID SERVICE DATA LENGTH", len(payload), payload)
            return
        
        self.opCode           = payload[0]
        self.dataType         = payload[1]
        self.crownstoneId     = payload[2]
        self.switchState      = payload[3]
        self.flagBitmask      = payload[4]
        self.temperature      = Conversion.uint8_to_int8(payload[5])
        self.powerFactor      = float(Conversion.uint8_to_int8(payload[6])) / 127
        self.powerUsageReal   = float(Conversion.uint8_array_to_int16(payload[7:7+2])) / 8
        self.energyUsed       = Conversion.uint8_array_to_int32(payload[9:9+4]) * 64
        self.partialTimestamp = Conversion.uint8_array_to_int16(payload[13:13+2])
        self.validation       = Conversion.uint8_array_to_int16(payload[15:15+2])

    def isValid(self):
        if self.opCode == 3 and self.dataType == 0:
            return True
        
        return False

    def getDict(self):
        dict = {}
        
        dict["opCode"]           = self.opCode
        dict["dataType"]         = self.dataType
        dict["crownstoneId"]     = self.crownstoneId
        dict["switchState"]      = self.switchState
        dict["flagBitmask"]      = self.flagBitmask
        dict["temperature"]      = self.temperature
        dict["powerFactor"]      = self.powerFactor
        dict["powerUsageReal"]   = self.powerUsageReal
        dict["energyUsed"]       = self.energyUsed
        dict["partialTimestamp"] = self.partialTimestamp
        dict["validation"]       = self.validation
        
        return dict