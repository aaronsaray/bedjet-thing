from boot import status_led
from bedjet_thing.wifi_setup import WifiSetup
from bedjet_thing.config import Config
from bedjet_thing.app import App

status_led.action()
config = Config()
wifi = WifiSetup(config)
App(config, wifi)
status_led.done()
