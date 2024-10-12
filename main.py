from boot import status_led
from src.microdot import Microdot
from src.wifi_setup import WifiSetup
from src.app import App

status_led.action()

wifi = WifiSetup()
App(wifi.wifi_connection)

status_led.done()
