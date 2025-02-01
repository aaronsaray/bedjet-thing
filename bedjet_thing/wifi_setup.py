import network
import time
import json
import os
from time import sleep
from bedjet_thing.debug import Debug

class WifiSetup:
    SSID = 'BedJetThing'
    PASSWORD = 'BedJetThing'
    AUTHMODE = 3
    SETTINGS_FILE = 'bedjet-thing.json'

    ip = ''
    connected_to_wifi = False

    def __init__(self):
        self.wifi_radio = network.WLAN(network.STA_IF)
        self.access_point = network.WLAN(network.AP_IF)
        network.hostname('BedJetThing')
        self.start_wifi()

    def start_wifi(self):
        if self.has_settings_file():
            Debug.log('Has settings file: connecting to wifi')
            self.connected_to_wifi = True
            self.connect_to_wifi()
        else:
            Debug.log('No settings file: starting access point')
            self.start_access_point()
    
    def start_access_point(self):
        self.wifi_radio.active(False) # disconnect    

        self.access_point.active(True)
        self.access_point.config(essid = self.SSID, password = self.PASSWORD, authmode = self.AUTHMODE)
        Debug.log('Access point started')

    def get_available_ssids(self):
        self.wifi_radio.active(True)
        ssids = set()

        for ssid, *_ in self.wifi_radio.scan():
            decoded = ssid.decode('utf-8')
            if decoded:
                ssids.add(decoded)

        self.wifi_radio.active(False)

        return ssids
    
    def provision(self, ssid, password):
        Debug.log('Attempting to connect to ssid ' + ssid)

        self.wifi_radio.active(True)
        self.wifi_radio.connect(ssid, password)
        
        for _ in range(100):
            if self.wifi_radio.isconnected():
                Debug.log('Connected to wifi')
                Debug.log(self.wifi_radio.ifconfig())

                self.ip = self.wifi_radio.ifconfig()[0]

                content = json.dumps({'ssid': ssid, 'password': password})
                file = open(self.SETTINGS_FILE, 'w')
                file.write(content)
                file.close()
                
                return True
            else:
                time.sleep_ms(100)
        
        Debug.log('Unable to connect')        
        
        self.wifi_radio.disconnect()
        self.wifi_radio.active(False)
        return False

    def has_settings_file(self):
        return self.SETTINGS_FILE in os.listdir();

    def connect_to_wifi(self):
        self.access_point.active(False)

        file = open(self.SETTINGS_FILE, 'r')
        c = json.load(file)
        self.wifi_radio.active(True)
        self.wifi_radio.connect(c['ssid'], c['password'])

        while not self.wifi_radio.isconnected():
            sleep(0.1)

        Debug.log('wifi connected: ' + self.wifi_radio.ifconfig()[0])