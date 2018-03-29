from BluenetLib.lib.packets.seriviceDataParsers.opCode3.opCode3_type1 import parseOpcode3_type1
from BluenetLib.lib.util.Conversion import Conversion


def parseOpcode3_type3(serviceData, data):
    if len(data) == 17:
        parseOpcode3_type1(serviceData, data)

        # apply differences between type 1 and type 4
        serviceData.stateOfExternalCrownstone = True
        serviceData.powerUsageReal = 0
        serviceData.validation = Conversion.uint8_array_to_uint16([data[15], data[16]])
