import aioble
import asyncio
from bluetooth import UUID

async def main():
    bedJetResult = None

    async with aioble.scan(duration_ms=5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            if result.name() is 'BEDJET_V3':
                bedJetResult = result

    if not bedJetResult:
        raise RuntimeError('Can not find the bedjet v3 device')

    try:
        connection = await bedJetResult.device.connect(timeout_ms=2000)
        print('Connected')
    except asyncio.TimeoutError:
        raise RuntimeError('Timeout Connecting')
    
    async with connection:
        print('connect to the service')
        service = await connection.service(UUID('00001000-bed0-0080-aa55-4265644a6574'))
        print('connected')

        print('getting control characteristic')
        control_characteristic = await service.characteristic(UUID('00002004-bed0-0080-aa55-4265644a6574'))
        print('retrieved', control_characteristic)

        print('attempting to set mode')
        value = bytearray(b'\x01\x02')
        control_characteristic.write(value)
        print('sent')

asyncio.run(main())



# import gc
# from boot import status_led
# # from bedjet_thing.wifi_setup import WifiSetup
# # from bedjet_thing.app import App
# import aioble
# import asyncio
# from bluetooth import UUID
# import struct

# gc.enable()
# gc.collect()
# gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

# status_led.action()

# # wifi = WifiSetup()
# # App(wifi.wifi_radio, wifi.write_credentials, wifi.clear_credentials)

# status_led.done()

# def _decode_temperature(data):
#     return struct.unpack("<h", data)[0] / 100

# def handle_data(handle, value):
#     print('handle', handle)
#     print('value', value)

# async def main():
#     bedJetResult = None

#     async with aioble.scan(duration_ms=5000, interval_us=30000, window_us=30000, active=True) as scanner:
#         async for result in scanner:
#             if result.name() is 'BEDJET_V3':
#                 bedJetResult = result

#     if not bedJetResult:
#         raise RuntimeError('Can not find the bedjet v3 device')

# #    print(list(bedJetResult.services())) # 00001000-bed0-0080-aa55-4265644a6574


#     BEDJET_COMMAND_UUID = '00002004-bed0-0080-aa55-4265644a6574'
#     BEDJET_SUBSCRIPTION_UUID = '00002000-bed0-0080-aa55-4265644a6574'

#     try:
#         connection = await bedJetResult.device.connect(timeout_ms=2000)
#         print('Connected')
#     except asyncio.TimeoutError:
#         raise RuntimeError('Timeout Connecting')
    
#     async with connection:
#         print('connect to the service')
#         service = await connection.service(UUID('00001000-bed0-0080-aa55-4265644a6574'))
#         print('connected')
#         await asyncio.sleep(3)

#         # print('getting device name characteristic')
#         # device_name_characteristic = await service.characteristic(UUID('00002001-bed0-0080-aa55-4265644a6574'))
#         # print('retrieved')

#         # print('getting device name')
#         # device_name = await device_name_characteristic.read(timeout_ms=1000)
#         # print('name', device_name.decode())

#         # print('getting temperature characteristic')
#         # temperature_characteristic = await service.characteristic(UUID('00002000-bed0-0080-aa55-4265644a6574'))
#         # print('retrieved', temperature_characteristic)

#         # this is how you keep it active
#         # await temperature_characteristic.subscribe()
#         # while True:
#         #     data = await temperature_characteristic.notified()
#         #     print('raw value', data)
#         #     await asyncio.sleep(1)

#         # print('getting the notified value')
#         # data = await temperature_characteristic.notified(timeout_ms=1000)
#         # print('raw value', data)
#         # value = data
#         # print('attempt', round(((int(value[7]) - 0x26) + 66) - ((int(value[7]) - 0x26) / 9)))

#         # if value[14] == 0x50 and value[13] == 0x14:
#         #     print('it is off')

#         print('getting control characteristic')
#         control_characteristic = await service.characteristic(UUID('00002004-bed0-0080-aa55-4265644a6574'))
#         print('retrieved', control_characteristic)
#         # confirmed 8 - so we can write - print('properties', control_characteristic.properties)

#         await asyncio.sleep(3)

#         print('attempting to set mode')
#         # string = "0102" # represents 0x01 and 0x02
#         # value = bytearray.fromhex(string)
#         # value = 0x0102
#         one = const(0x01)
#         two = const(0x02)
#         value = struct.pack('<h', one, two)
#         control_characteristic.write(value)
#         await asyncio.sleep(3)
#         print('sent')
#         # there are some descriptors in the control service
#         # async for descriptor in control_characteristic.descriptors():
#         #     print('descriptor', descriptor)
#         #print('attempting to subscribe to temp')
#         # temperature_characteristic.subscribe()

#         # while connection.is_connected():
#         #     value = await temperature_characteristic.read()
#         #     print('raw value', _decode_temperature(value))
#         #     await asyncio.sleep_ms(1000)



# # #        temp_char.subscribe(UUID('00002000-bed0-0080-aa55-4265644a6574'), handle_data)

# #         # await temp_char.subscribe(notify=True)
# #         # while True:
# #         #     data = await temp_char.notified()
# #         await temp_char.subscribe(indicate=True)
# #         while True:
# #             data = await temp_char.indicated()
# #             print('data', data)

# #         # not supported
# #         # print('notification')
# #         # data = await characteristic.notified(timeout_ms=1000)
# #         # print('data', data)

# #         # not supported
# #         # print('indicated')
# #         # data = await characteristic.indicated(timeout_ms=1000)
# #         # print('data', data)

# # #    print('connected to service')



# asyncio.run(main())