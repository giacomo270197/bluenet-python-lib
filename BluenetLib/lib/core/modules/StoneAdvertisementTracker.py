import time
from threading import Timer
import threading

AMOUNT_OF_REQUIRED_MATCHES = 2

class StoneAdvertisementTracker:
    rssiHistory = None
    rssi = None
    name = ""
    address = None
    crownstoneId = 0
    lastUpdate = 0
    avgRssi = 0
    cleanupCallback = None
    uniqueIdentifier = 0
    verified = False
    dfu = False
    
    # config
    timeoutDuration     = 4  # seconds
    rssiTimeoutDuration = 3  # seconds
    consecutiveMatches  = 0
    
    timeoutTime = 0
    rssiTimeoutList = None
    _lock = None
    
    def __init__(self, cleanupCallback):
        self.rssiHistory = {}
        self.rssiTimeoutList = []
        self.cleanupCallback = cleanupCallback
        self._lock = threading.Lock()


    def tick(self):
        now = time.time()
        # check time in self.timeoutTime with current time
        if self.timeoutTime <= now:
            self.cleanupCallback()
            return

        # loop over rssi list
        remainingList = []
        for measurement in self.rssiTimeoutList:
            if measurement["timeoutTime"] <= now:
                del self.rssiHistory[measurement["key"]]
            else:
                remainingList.append(measurement)

        self.rssiTimeoutList = None
        self.rssiTimeoutList = remainingList
        self.avgRssi = self.calculateRssiAverage()



    def update(self, advertisement):
        self.name = advertisement.name
        self.address = advertisement.address
        self.avgRssi = advertisement.rssi
        if advertisement.isCrownstoneFamily():
            self.handlePayload(advertisement)
                
                
    def handlePayload(self, advertisement):
        # this field can be manipulated during the loop in calculate. To avoid this, we lock the threads for the duration of the loop
        with self._lock:
            self.rssi = advertisement.rssi
        
            now = time.time()
            
            self.lastUpdate = now
    
            self.rssiHistory[now] = self.rssi
        
            if advertisement.isInDFUMode():
                self.verified = True
                self.dfu = True
                self.consecutiveMatches = 0
            else:
                self.verify(advertisement.serviceData)
            
            self.avgRssi = self.calculateRssiAverage()
            self.timeoutTime = now + self.timeoutDuration
            self.rssiTimeoutList.append({"key": now, "timeoutTime": now + self.rssiTimeoutDuration})


    # check if we consistently get the ID of this crownstone.
    def verify(self, serviceData):
        if serviceData.isInSetupMode():
            self.verified = True
            self.consecutiveMatches = 0
        else:
            if serviceData.dataReadyForUse == False:
                self.invalidateDevice(serviceData)
            else:
                if self.uniqueIdentifier != serviceData.uniqueIdentifier:
                    if serviceData.validation != 0 and serviceData.opCode == 5:
                        if serviceData.validation == 0xFA and serviceData.dataType != 1: # datatype 1 is the error packet
                            self.addValidMeasurement(serviceData)
                        elif serviceData.validation != 0xFA and serviceData.dataType != 1: # datatype 1 is the error packet
                            self.invalidateDevice(serviceData)
                    elif serviceData.validation != 0 and serviceData.opCode == 3:
                        if serviceData.dataType != 1:
                            if serviceData.validation == 0xFA:
                                self.addValidMeasurement(serviceData)
                            elif serviceData.validation != 0xFA:
                                self.invalidateDevice(serviceData)
                        else:
                            pass # do nothing, skip these messages (usually error states)
                    else:
                        if not serviceData.stateOfExternalCrownstone:
                            if serviceData.crownstoneId == self.crownstoneId:
                                self.addValidMeasurement(serviceData)
                            else:
                                self.invalidateDevice(serviceData)
        
        self.uniqueIdentifier = serviceData.uniqueIdentifier
        

    
    def addValidMeasurement(self, serviceData):
        if self.consecutiveMatches >= AMOUNT_OF_REQUIRED_MATCHES:
            self.verified = True
            self.consecutiveMatches = 0
        else:
            self.consecutiveMatches += 1
        
        self.crownstoneId = serviceData.crownstoneId



    def invalidateDevice(self, serviceData):
        if not serviceData.stateOfExternalCrownstone:
            self.crownstoneId = serviceData.crownstoneId
        
        self.consecutiveMatches = 0
        self.verified = False



    def calculateRssiAverage(self):
        count = 0
        total = 0

        for key, rssi in self.rssiHistory.items():
            total = total + rssi
            count += 1

        if count > 0:
            return total / float(count)
        else:
            return 0
        
        
        