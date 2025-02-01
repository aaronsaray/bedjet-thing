import network
from time import sleep
from bedjet_thing.debug import Debug

class WifiSetup:
    SSID = 'BedJetThing'
    PASSWORD = 'BedJetThing'
    AUTHMODE = 3

    def __init__(self):
        self.wifi_radio = network.WLAN(network.STA_IF)
        self.access_point = network.WLAN(network.AP_IF)
        network.hostname('BedJetThing')
        self.start_wifi()

    def start_wifi(self):
        self.start_access_point()

    def start_access_point(self):
        self.wifi_radio.active(False) # disconnect    

        self.access_point.active(True)
        self.access_point.config(essid = self.SSID, password = self.PASSWORD, authmode = self.AUTHMODE)
        Debug.log('Access point started')
