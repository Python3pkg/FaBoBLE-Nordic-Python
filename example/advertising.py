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
import RPi.GPIO as GPIO

port = '/dev/ttyAMA0'
rate = 115200

# Button Brick接続ピン
BUTTON_PIN = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)
# ボタンの押下状況取得用
buttonState = 0
isFirst = False

print("BLE Advertise Sample")

print("BLE Enable")
# BLE設定、初期処理
ble = FaBoBLE_Nordic.Nordic(port, rate)

# デバッグ有効
#ble.setDebug()

uuid  = [0x00, 0x01, 0x12, 0x23, 0x34, 0x45, 0x56, 0x67,
         0x78, 0x89, 0x9a, 0xab, 0xbc, 0xcd, 0xde, 0xef]
major = [0xfe, 0xed]
minor = [0xdc, 0xcb]

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

while True:
    ble.tick()

    # ボタンの押下状況を取得
    buttonState = GPIO.input(BUTTON_PIN)
    # ボタン押下判定
    if buttonState:
        # ボタン押下時初回のみ実行
        if isFirst == False:
            isFirst == True
            # アドバタイズ状態判定
            if ble.isAdvertising()==False:
                # アドバタイズ開始
                if ble.startAdv():
                    print("Success:Start Beacon advertising")
                else:
                    print("Failed:Start Beacon advertising")
            else:
                # アドバタイズ終了
                if ble.stopAdv():
                    print("Success:Stop Beacon advertising")
                else:
                    print("Failed:Stop Beacon advertising")
    else:
        isFirst = False
