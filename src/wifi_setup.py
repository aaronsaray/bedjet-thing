import os
import network
import json
from time import sleep

class WifiSetup:
    SETTINGS_FILE = 'bedjet-thing.json'
    SSID = 'BedJetThing'
    PASSWORD = 'BedJetThing'
    AUTHMODE = 3

    def debug(self, message):
        print('DEBUG: ', end='')
        print(message)

    def __init__(self):
        self.wifi_connection = None
        self.startWifi()
        
    def startWifi(self):
        if self.has_settings_file():
            self.debug('has settings file')
            self.connectToWiFi()
        else:
            self.debug('no settings file')
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
        self.debug('internal wifi started')

    def connectToWiFi(self):
        file = open(self.SETTINGS_FILE, 'r')
        c = json.load(file)

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(c['ssid'], c['password'])

        while not wlan.isconnected():
            sleep(0.1)

        self.debug('wifi connected: ' + wlan.ifconfig()[0])
