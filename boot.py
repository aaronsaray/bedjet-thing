from machine import Pin
import json
import network
import esp
import gc
import asyncio
import os

async def loading_led():
  while True:
    led.on()
    await asyncio.sleep(0.1)
    led.off()
    await asyncio.sleep(0.1)


async def success_led():
  led.on()
  await asyncio.sleep(3)
  led.off()


async def error_led():
  led.on()
  await asyncio.sleep(5)
  led.off()


async def connect_to_wifi(ssid, password):
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect(ssid, password)

  while not wlan.isconnected():
    await asyncio.sleep(0.1)

  print('WLAN Connection successful')
  print(wlan.ifconfig())


async def main():
  esp.osdebug(None)
  gc.collect()

  loading_task = asyncio.create_task(loading_led())

  if settingsFile in os.listdir():
    file = open(settingsFile, 'r')
    c = json.load(file)

    await connect_to_wifi(c['ssid'], c['password'])

    loading_task.cancel()
    await success_led()
  else:
    loading_task.cancel()
    await error_led()


led = Pin(2, Pin.OUT)
settingsFile = 'bedjet.json'

asyncio.run(main())