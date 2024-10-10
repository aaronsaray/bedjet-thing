import esp
import gc
import os
import network

class InitialSetup:
    SETTINGS_FILE = 'bedjet.json'
    SSID = 'ESP32BedJet3'
    PASSWORD = 'ESP32BedJet3'
    AUTHMODE = 3

    def __init__(self):
        esp.osdebug(None)
        gc.collect()
        self.wifi_connection = ''
        self.startWifi()
        
    def startWifi(self):
        if self.has_settings_file():
            pass
        else:
            self.startInternalWiFi()

    def has_settings_file(self):
        return self.SETTINGS_FILE in os.listdir();

    def startInternalWiFi(self):
        self.wifi_connection = network.WLAN(network.STA_IF)
        self.wifi_connection.active(False) # disconnect    

        # generate the access point
        access_point = network.WLAN(network.AP_IF)
        access_point.active(True)
        access_point.config(essid = self.SSID, password = self.PASSWORD, authmode = self.AUTHMODE)
