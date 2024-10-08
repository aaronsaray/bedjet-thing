try:
  import usocket as socket
except:
  import socket

import json
import network
import esp
import gc
import os
from time import sleep

settingsFile = 'bedjet.json'



def connect_to_wifi(ssid, password):
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect(ssid, password)

  while not wlan.isconnected():
    sleep(0.1)

  debug('Wifi Connected')
  debug(wlan.ifconfig())



def get_web_response():
  with open("index.html", "r") as index:
    html = index.read()
    index.close()
  return html



def web_server():
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(5)
  except OSError as e:
    debug('Failed to open socket')
    debug(e)
    return

  while True:
    try:
      if gc.mem_free() < 102000:
        gc.collect()
      conn, addr = s.accept()
      conn.settimeout(3.0)

      request = conn.recv(1024)
      conn.settimeout(None)
      request = str(request)

      debug('Incoming request')
      debug(request)

      response = get_web_response()
      conn.send('HTTP/1.1 200 OK\n')
      conn.send('Content-Type: text/html\n')
      conn.send('Connection: close\n\n')
      conn.sendall(response)
      conn.close()
    except OSError as e:
      conn.close()
      debug('Connection closed error')
      debug(e)



def main():
  esp.osdebug(None)
  gc.collect()

  if settingsFile in os.listdir():
    led_action()
    file = open(settingsFile, 'r')
    c = json.load(file)

    connect_to_wifi(c['ssid'], c['password'])

  led_done()

  web_server()

main()
