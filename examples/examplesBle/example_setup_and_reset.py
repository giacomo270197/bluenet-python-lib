#!/usr/bin/env python3


import time

from BluenetLib.BLE import BluenetBle

print("===========================================\n\nStarting Example\n\n===========================================")
print("This is an example that performs the setup of a Crownstone, and then factory resets it again.\n")

# Initialize the Bluetooth Core.
# Fill in the correct hciIndex, see the readme.
core = BluenetBle(hciIndex=0)


print("We're loading some default encryption keys into the library: \"adminKeyForCrown\", \"memberKeyForHome\", \"guestKeyForOther\".\n")
core.setSettings("adminKeyForCrown", "memberKeyForHome", "guestKeyForOther")

print("Searching for the nearest setup Crownstone. This is with a threshold of RSSI: -100, so it will use any available setup Crownstones.\n")
print("Keep in mind that the RSSI in setup mode is low to protect the key exchange so even if you're close, it can still be around -80.\n")

# get the nearest crownstone in setup mode. We expect it to be atleast within the -70db range
nearestStone = core.getNearestSetupCrownstone(rssiAtLeast=-100, returnFirstAcceptable=True)

print("Search Results:", nearestStone)

if nearestStone is not None:
    # setup the nearest Crownstone if we can find one
    print("Starting setup on ", nearestStone["address"])
    core.setupCrownstone(
        nearestStone["address"],
        crownstoneId=1,
        meshAccessAddress="4f745905",
        ibeaconUUID="1843423e-e175-4af0-a2e4-31e32f729a8a",
        ibeaconMajor=123,
        ibeaconMinor=456
    )
    
    # wait for setup to finish and the crownstone to reboot
    print("Sleeping until Crownstone is in Normal mode and ready.")
    time.sleep(10)
    
    # reset the Crownstone back into setup mode
    print("Starting the Factory Reset Process")
    core.connect(nearestStone["address"])
    print("Command factory reset")
    core.control.commandFactoryReset()
    time.sleep(1)
    # print("command disconnect")
    # core.control.disconnect()
else:
    print("No stones found in setup mode...")
# clean up all pending processes
print("Core shutdown")
core.shutDown()

print("===========================================\n\nFinished Example\n\n===========================================")