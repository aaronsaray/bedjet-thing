from boot import status_led
from bedjet_thing.wifi_setup import WifiSetup
from bedjet_thing.app import App

status_led.action()
App()
status_led.done()
