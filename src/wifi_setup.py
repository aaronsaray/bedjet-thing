import os
import network
import json
from time import sleep

class WifiSetup:
    SETTINGS_FILE = 'bedjet-thing.json'
    SSID = 'BedJetThing'
    PASSWORD = 'BedJetThing'
    AUTHMODE = 3

    def __init__(self):
        self.wifi_radio = network.WLAN(network.STA_IF)
        self.access_point = network.WLAN(network.AP_IF)
        self.start_wifi()

    def debug(self, message):
        print('DEBUG: ', end='')
        print(message)

    def start_wifi(self):
        if self.has_settings_file():
            self.debug('has settings file')
            self.connect_to_wifi()
        else:
            self.debug('no settings file')
            self.start_access_point()

    def has_settings_file(self):
        return self.SETTINGS_FILE in os.listdir();

    def write_credentials(self, ssid, password):
        content = json.dumps({'ssid': ssid, 'password': password})
        file = open(self.SETTINGS_FILE, 'w')
        file.write(content)
        file.close()

    def start_access_point(self):
        self.wifi_radio.active(False) # disconnect    

        self.access_point.active(True)
        self.access_point.config(essid = self.SSID, password = self.PASSWORD, authmode = self.AUTHMODE)
        self.debug('access point started')

    def connect_to_wifi(self):
        self.access_point.active(False)

        file = open(self.SETTINGS_FILE, 'r')
        c = json.load(file)
        self.wifi_radio.active(True)
        self.wifi_radio.connect(c['ssid'], c['password'])

        while not self.wifi_radio.isconnected():
            sleep(0.1)

        self.debug('wifi connected: ' + self.wifi_radio.ifconfig()[0])
