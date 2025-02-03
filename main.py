from boot import status_led
from bedjet_thing.wifi_setup import WifiSetup
from bedjet_thing.config import Config
from bedjet_thing.bluetooth import Bluetooth
from bedjet_thing.app import App

## To Verify
# import json
# with open('bedjet-thing.json', 'r') as f:
#     c = json.load(f)
#     print('config file')
#     print(c)

## To Reset on BT fuckery
# print ('resetting file')
# import json
# ssid = 'MyWiFi2'
# password = 'mZm7Huc*Md'
# data = {'ssid': ssid, 'password': password}
# with open('bedjet-thing.json', 'w') as f:
#     json.dump(data, f)
#     f.close()
# print ('file reset')

status_led.action()
config = Config()
wifi = WifiSetup(config)
bluetooth = Bluetooth(config)
App(config, wifi, bluetooth)
status_led.done()
