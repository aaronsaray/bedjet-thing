import os
import json
from bedjet_thing.debug import Debug

class Config:
    CONFIG_FILE = 'bedjet-thing.json'
    
    has_config = False
    ssid = ''
    password = ''

    def __init__(self):
        self.has_config = self.CONFIG_FILE in os.listdir();
        Debug.log('Has config file: ' + str(self.has_config))

        if self.has_config:
            file = open(self.CONFIG_FILE, 'r')
            c = json.load(file)
            self.ssid = c['ssid']
            self.password = c['password']

    def store_wifi(self, ssid, password):
        content = json.dumps({'ssid': ssid, 'password': password})
        file = open(self.CONFIG_FILE, 'w')
        file.write(content)
        file.close()
