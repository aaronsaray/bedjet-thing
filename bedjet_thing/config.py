import os
import json
from bedjet_thing.debug import Debug

class Config:
    CONFIG_FILE = 'bedjet-thing.json'
    
    has_config = False
    has_wifi = False
    has_bluetooth = False

    ssid = ''
    password = ''
    uuid = ''

    def __init__(self):
        self.has_config = self.CONFIG_FILE in os.listdir();
        Debug.log('Has config file: ' + str(self.has_config))

        if self.has_config:
            file = open(self.CONFIG_FILE, 'r')
            c = json.load(file)

            self.ssid = c['ssid']
            self.password = c['password']
            self.has_wifi = True

            if 'uuid' in c:
                self.has_bluetooth = True
                self.uuid = bytes.fromhex(c['uuid'])

            file.close()

    def store_wifi(self, ssid, password):
        data = {'ssid': ssid, 'password': password}
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(data, f)
            f.close()

    def store_bluetooth(self, bytesUuid):
        file = open(self.CONFIG_FILE, 'r')
        data = json.load(file)
        file.close()

        data['uuid'] = bytesUuid.hex()

        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(data, f)
            f.close()

    def clear(self): 
        os.unlink(self.CONFIG_FILE)