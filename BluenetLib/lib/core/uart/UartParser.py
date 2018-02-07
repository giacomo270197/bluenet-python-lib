
from BluenetLib.lib.core.uart.UartTypes import UartRxType
from BluenetLib.lib.core.uart.uartPackets.CurrentSamplesPacket import CurrentSamplesPacket
from BluenetLib.lib.core.uart.uartPackets.MeshStatePacket import MeshStatePacket
from BluenetLib.lib.core.uart.uartPackets.PowerCalculationPacket import PowerCalculationPacket
from BluenetLib.lib.core.uart.uartPackets.ServiceDataPacket import ServiceDataPacket
from BluenetLib.lib.core.uart.uartPackets.VoltageSamplesPacket import VoltageSamplesPacket

from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.topics.DevTopics import DevTopics
from BluenetLib.lib.topics.SystemTopics import SystemTopics


class UartParser:
    def __init__(self):
        BluenetEventBus.subscribe(SystemTopics.uartNewPackage, self.parse)

    def parse(self, dataPacket):

        opCode = dataPacket.opCode

        if opCode == UartRxType.MESH_STATE_0 or opCode == UartRxType.MESH_STATE_1:
            # unpack the mesh packet
            meshPacket = MeshStatePacket(dataPacket.payload)

            # have each stone in the meshPacket broadcast it's state
            for stoneState in meshPacket.stoneStates:
                stoneState.broadcastState()
                
        elif opCode == UartRxType.SERVICE_DATA:
            serviceData = ServiceDataPacket(dataPacket.payload)
            if serviceData.isValid():
                BluenetEventBus.emit(DevTopics.newServiceData, serviceData.getDict())
  
        elif opCode == UartRxType.POWER_LOG_CURRENT:
            # type is CurrentSamples
            parsedData = CurrentSamplesPacket(dataPacket.payload)
            BluenetEventBus.emit(DevTopics.newCurrentData, parsedData.getDict())
            
        elif opCode == UartRxType.POWER_LOG_VOLTAGE:
            # type is VoltageSamplesPacket
            parsedData = VoltageSamplesPacket(dataPacket.payload)
            BluenetEventBus.emit(DevTopics.newVoltageData, parsedData.getDict())
            
        elif opCode == UartRxType.POWER_LOG_FILTERED_CURRENT:
            # type is CurrentSamples
            parsedData = CurrentSamplesPacket(dataPacket.payload)
            BluenetEventBus.emit(DevTopics.newFilteredCurrentData, parsedData.getDict())
            
        elif opCode == UartRxType.POWER_LOG_FILTERED_VOLTAGE:
            # type is VoltageSamplesPacket
            parsedData = VoltageSamplesPacket(dataPacket.payload)
            BluenetEventBus.emit(DevTopics.newFilteredVoltageData, parsedData.getDict())
            
        elif opCode == UartRxType.POWER_LOG_POWER:
            # type is PowerCalculationsPacket
            parsedData = PowerCalculationPacket(dataPacket.payload)
            BluenetEventBus.emit(DevTopics.newCalculatedPowerData, parsedData.getDict())
            
        else:
            print("Unknown OpCode", opCode)


