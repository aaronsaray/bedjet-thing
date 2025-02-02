from boot import status_led
from bedjet_thing.wifi_setup import WifiSetup
from bedjet_thing.config import Config
from bedjet_thing.bluetooth import Bluetooth
from bedjet_thing.app import App

status_led.action()
config = Config()
wifi = WifiSetup(config)
bluetooth = Bluetooth(config)
App(config, wifi, bluetooth)
status_led.done()
