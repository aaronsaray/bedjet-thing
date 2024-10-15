import gc
from boot import status_led
from src.wifi_setup import WifiSetup
from src.app import App

gc.enable()

status_led.action()

wifi = WifiSetup()
App(wifi.wifi_radio, wifi.write_credentials, wifi.clear_credentials)

status_led.done()
