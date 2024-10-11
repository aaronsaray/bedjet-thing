from src.initial_setup import InitialSetup
from src.web_server import WebServer

status_led.action()
setup = InitialSetup()
WebServer(status_led, setup.wifi_connection, setup.has_settings_file())