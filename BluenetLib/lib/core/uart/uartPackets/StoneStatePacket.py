import time

from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.topics.SystemTopics import SystemTopics
from BluenetLib.lib.util.Conversion import Conversion
from BluenetLib.lib.util.Timestamp  import reconstructTimestamp

STONE_STATE_PACKET_SIZE = 14

class StoneStatePacket:

    def __init__(self, meshStateItem):
        self.type = 0
        self.crownstoneId = 0
        self.switchState = 0
        self.flagBitMask = 0
        self.temperature = 0
        self.powerFactor = 0
        self.powerUsageReal = 0
        self.powerUsageApparent = 0
        self.energyUsed = 0
        self.partialTimestamp = 0
        self.timestamp = 0
        self.deprecated = False
        
        if len(meshStateItem) != STONE_STATE_PACKET_SIZE:
            print("ERROR: Invalid length of StoneStatePacket", len(meshStateItem), meshStateItem)

        self.type = meshStateItem[0]

        if self.type is 0 or self.type is 2:
            self.parseState(meshStateItem[1:])
        else:
            print("Got error payload. Ignoring for now")


    def parseState(self, meshStateItemState):
        self.crownstoneId       = meshStateItemState[0]
        self.switchState        = meshStateItemState[1]
        self.flagBitMask        = meshStateItemState[2]
        self.temperature        = meshStateItemState[3]
        self.powerFactor        = float(meshStateItemState[4]) / 127
        self.powerUsageReal     = float(Conversion.uint8_array_to_int16(meshStateItemState[5:7])) / 8
        if self.powerFactor == 0:
            self.powerFactor = 1.0
        self.powerUsageApparent = self.powerUsageReal / self.powerFactor
        self.energyUsed         = Conversion.uint8_array_to_int32(meshStateItemState[7:11])
        self.partialTimestamp   = Conversion.uint8_array_to_uint16(meshStateItemState[11:13])
        self.timestamp          = reconstructTimestamp(time.time(), self.partialTimestamp)

        if self.crownstoneId == 0:
            self.deprecated = True

    def constuctTimestamp(self):
        pass

    def broadcastState(self):
        if self.deprecated:
            return

        # tell the system this advertisement.
        BluenetEventBus.emit(SystemTopics.stateUpdate, (self.crownstoneId, self))

    def getDict(self):
        data = {}

        data["id"]                 = self.crownstoneId
        data["switchState"]        = self.switchState
        data["flagBitMask"]        = self.flagBitMask
        data["temperature"]        = self.temperature
        data["powerFactor"]        = self.powerFactor
        data["powerUsageReal"]     = self.powerUsageReal
        data["powerUsageApparent"] = self.powerUsageApparent
        data["energyUsed"]         = self.energyUsed
        data["timestamp"]          = self.timestamp

        return data