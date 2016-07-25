# coding: utf-8
## @package FaBoBLE_Nordic
#  This is a library for the FaBo BLE_Nordic Brick.
#
#  http://fabo.io/307.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import FaBoBLE_Nordic
import sys

port = '/dev/ttyAMA0'
rate = 115200
print "BLE Nordic SCAN sample"
print "BLE Enable"
ble = FaBoBLE_Nordic.Nordic(port, rate)

#ble.setDebug()

ble.startScan()

while True:
    # BLE内部処理のためloop内で呼び出してください
    ble.tick()

    buff =  ble.getScanData()
    if buff["rssi"]!=0:
        print "Handle:%04x" % long(buff["handle"]),

        print " AddrType:%1x" % buff["addrtype"],

        print " Address:",
        for i in range(6):
            sys.stdout.write('%02x' % buff["address"][i])

        print ' RSSI:%02d' % buff["rssi"],
        if buff["rssi"] > -100:
            sys.stdout.write("  ")

        print " Data:",
        for i in range(buff["data_len"]):
            sys.stdout.write('%02x' % buff["data"][i])
        print
