from enum import Enum

class DevTopics(Enum):
    newServiceData = "newServiceData"  # data is dictionary: {
    #                        "opCode": int
    #                        "dataTyle": int
    #                        "crownstoneId": int
    #                        "switchState": int
    #                        "flagBitmask": int
    #                        "temperature": int
    #                        "powerFactor": int
    #                        "powerUsageReal": int
    #                        "energyUsed": int
    #                        "partialTimestamp": int
    #                        "validation": int
    #                     }
    newCurrentData = "newCurrentData"  # data is dictionary: { crownstoneId: int, type: 'current', data: [(time, data point)] }
    newVoltageData = "newVoltageData"  # data is dictionary: { crownstoneId: int, type: 'voltage', data: [(time, data point)] }
    newFilteredCurrentData = "newFilteredCurrentData"  # data is dictionary: { crownstoneId: int, type: 'current', data: [(time, data point)] }
    newFilteredVoltageData = "newFilteredVoltageData"  # data is dictionary: { crownstoneId: int, type: 'voltage', data: [(time, data point)] }
    newCalculatedPowerData = "newCalculatedPowerData"  # data is dictionary: {
    #                        "crownstoneId": int,
    #                        "currentRmsMA": int,
    #                        "currentRmsMedianMA": int,
    #                        "filteredCurrentRmsMA": int,
    #                        "filteredCurrentRmsMedianMA": int,
    #                        "avgZeroVoltage": int,
    #                        "avgZeroCurrent": int,
    #                        "powerMilliWattApparent": int,
    #                        "powerMilliWattReal": int,
    #                        "avgPowerMilliWattReal": int
    #                     }
