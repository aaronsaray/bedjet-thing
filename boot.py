try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network
import esp
import gc
import time
import asyncio

led = Pin(2, Pin.OUT)
ssid = 'MonkFish'
password = 'chompers99*'


async def blink_led():
  while True:
    led.on()
    await asyncio.sleep(0.1)
    led.off()
    await asyncio.sleep(0.1)


async def connect_to_wifi():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect(ssid, password)

  while not wlan.isconnected():
    await asyncio.sleep(0.1)

  led.off()


async def main():
  esp.osdebug(None)
  gc.collect()

  blink_task = asyncio.create_task(blink_led())

  await connect_to_wifi()

  blink_task.cancel()


asyncio.run(main())