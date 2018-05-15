from BluenetLib.lib.util.Conversion import Conversion


class ResultPacket:
    type = 0
    opCode = 0
    length = 0
    payload = []
    
    valid = False
    
    def __init__(self, data):
        if len(data) >= 4:
            self.valid = True
            self.type = data[0]
            self.opCode = data[1]
            self.length = Conversion.uint8_array_to_uint16([data[2], data[3]])
            totalSize = 4 + self.length
            if len(data) >= totalSize:
                self.payload = data[4:]
            else:
                self.valid = False
        else:
            self.valid = False
    
    
    def getUInt16Payload(self):
        if not self.valid:
            return 65535
    
        if self.length >= 2:
            return Conversion.uint8_array_to_uint16([self.payload[0], self.payload[1]])
        else:
            return 65535
    
    
