import aioble
from bedjet_thing.debug import Debug

class Bluetooth:
    def __init__(self, config):
        self.config = config

    async def provision(self):
        async with aioble.scan(duration_ms=5000, interval_us=30000, window_us=30000, active=True) as scanner:
            async for result in scanner:
                if result.name() is 'BEDJET_V3':
                    Debug.log('Found bedjet')
                    Debug.log(result)
                    return True

        Debug.log('Not found')
        return False