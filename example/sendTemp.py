# coding: utf-8
## @package FaBoBLE_Nordic
#  This is a library for the FaBo Nordic Brick.
#
#  http://fabo.io/307.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import FaBoBLE_Nordic
import time
import spidev
import sys

port = '/dev/ttyAMA0'
rate = 115200

# Button Brick接続ピン
TEMPPIN = 0

print("BLE Advertise Send Temperature Sample")

print("BLE Enable")
# BLE設定、初期処理
ble = FaBoBLE_Nordic.Nordic(port, rate)

# デバッグ有効
#ble.setDebug()

uuid  = [0x00, 0x01, 0x12, 0x23, 0x34, 0x45, 0x56, 0x67,
         0x78, 0x89, 0x9a, 0xab, 0xbc, 0xcd, 0xde, 0xef]
major = [0x01, 0x02]
minor = [0x00, 0x00]

ble.setBeaconUuid(uuid)
ble.setBeaconMajor(major)
ble.setBeaconMinor(minor)

# Beacon設定
if ble.setAdvData():
    print("Success:setAdvData()")
else:
    print("Failed:setAdvData()")

# アドバタイズ開始
if ble.startAdv():
    print("Success:Start Beacon advertising")
else:
    print("Failed:Start Beacon advertising")

# Set SPI
spi = spidev.SpiDev()
spi.open(0,0)

def readadc(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
    try:
        while True:
            data = readadc(TEMPPIN)
            volt = arduino_map(data, 0, 1023, 0, 5000)
            temp = arduino_map(volt, 300, 1600, -30, 100)
            print(("temp : {:4.1f} ".format(temp)))

            send_temp = int(temp)
            ble.setBeaconMinor([0, send_temp])
            if ble.setAdvData()==False:
                print("Failed :setAdvData()")

            time.sleep(5)

    except KeyboardInterrupt:
       spi.close()
       sys.exit(0)

