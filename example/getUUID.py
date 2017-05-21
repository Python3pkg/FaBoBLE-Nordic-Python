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

print("BLE Nordic SCAN GetUUID sample")
print("BLE Enable")
ble = FaBoBLE_Nordic.Nordic(port, rate)

#ble.setDebug()


ble.startScan()

while True:
    # BLE内部処理のためloop内で呼び出してください
    ble.tick()

    buff =  ble.getScanData()
    if buff["rssi"]!=0:
        print(' RSSI:%03d' % buff["rssi"], end=' ')
        if buff["rssi"] > -100:
            sys.stdout.write("  ")
        print(" arddrType:%1x" % buff["addrtype"], end=' ') 
        print(" UUID:", end=' ')
        for i in range(9,25):
            sys.stdout.write('%02x' % buff["data"][i])
        print(" MAJOR:",buff["data"][25]<<8 | buff["data"][26], end=' ')
        print(" MINOR:",buff["data"][27]<<8 | buff["data"][28], end=' ')
        print()
