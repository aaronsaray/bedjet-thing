import aioble
from bedjet_thing.debug import Debug

class Bluetooth:
    def __init__(self, config):
        self.config = config

    async def provision(self):
        found = False

        async with aioble.scan(duration_ms=3000, interval_us=30000, window_us=30000, active=True) as scanner:
            async for result in scanner:
                if result.name() is 'BEDJET_V3':
                    found = result.device.addr

        if found:
            Debug.log('Found Bluetooth: ' + found.hex())
            Debug.log(found)
            self.config.store_bluetooth(found)
            return True
        else:
            Debug.log('Did not find bluetooth')
            return False
        