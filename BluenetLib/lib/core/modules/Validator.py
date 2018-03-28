
from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.core.modules.StoneAdvertisementTracker import StoneAdvertisementTracker
from BluenetLib.lib.topics.SystemBleTopics import SystemBleTopics
from BluenetLib.lib.topics.Topics import Topics

import threading

class Validator:
    trackedCrownstones = {}
    tickTimer = None
    _lock = None

    def __init__(self):
        BluenetEventBus.subscribe(SystemBleTopics.rawAdvertisement, self.checkAdvertisement)
        self._lock = threading.Lock()
        self.scheduleTick()


    def scheduleTick(self):
        if self.tickTimer is not None:
            self.tickTimer.cancel()

        self.tickTimer = threading.Timer(1, lambda: self.tick())
        self.tickTimer.start()


    def tick(self):
        with self._lock:
            allKeys = []
            # we first collect keys because we might delete items from this list during ticks
            for key, trackedStone in self.trackedCrownstones.items():
                allKeys.append(key)

            for key in allKeys:
                self.trackedCrownstones[key].tick()

        self.scheduleTick()


    def removeStone(self, address):
        del self.trackedCrownstones[address]


    def checkAdvertisement(self, advertisement):
        if advertisement.address not in self.trackedCrownstones:
            self.trackedCrownstones[advertisement.address] = StoneAdvertisementTracker(lambda: self.removeStone(advertisement.address))
            
        self.trackedCrownstones[advertisement.address].update(advertisement)
        
        if self.trackedCrownstones[advertisement.address].verified:
            BluenetEventBus.emit(Topics.advertisement, advertisement.getDictionary())


    def shutDown(self):
        if self.tickTimer is not None:
            self.tickTimer.cancel()

        for address, tracker in self.trackedCrownstones.items():
            tracker.shutDown()
        