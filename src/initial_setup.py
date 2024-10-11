import esp
import gc
import os
import network
import json
from time import sleep

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
            print('has settings file')
            self.connectToWiFi()
            pass
        else:
            print('no settings file')
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

    def connectToWiFi(self):
        file = open(self.SETTINGS_FILE, 'r')
        c = json.load(file)

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(c['ssid'], c['password'])

        while not wlan.isconnected():
            sleep(0.1)

        print('WiFi Connected')
        print(wlan.ifconfig())
