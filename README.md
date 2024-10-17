# ESPHome ESP32 BedJet3 Control

* Connect device
* Visit https://micropython.org/download/ESP32_GENERIC/ and download latest firmware
* `brew install micropython`
* `ls /dev/tty.usb*` to see the usb name
* `esptool.py --port /dev/tty.usbserial-0001 erase_flash`
* `esptool.py --chip esp32 --port /dev/tty.usbserial-0001 --baud 921600 write_flash -z 0x1000 ESP32_GENERIC-20240602-v1.23.0.bin`
* `pipx install rshell`

Restart and it's going to run the code.

To deploy a file:

`rshell -p /dev/tty.usbserial-0001 cp boot.py /pyboard`
`rshell -p /dev/tty.usbserial-0001 cp main.py /pyboard`

Rsync the files over:
`rshell -p /dev/tty.usbserial-0001 rsync bedjet_thing /pyboard/bedjet_thing`
`rshell -p /dev/tty.usbserial-0001 rsync web /pyboard/web`

## Current Issues

* Only allowing my 2 access points because I haven't yet figured out how to escape shit properly.
* No back-end validation

## Compiling MPY

pip install mpy-cross
mpy-cross -march=xtensawin microdot.py ---- this made microdot.mpy and saved ram

## Packages

Install mpremote with pipx install mpremote

Then, mpremote mip install aioble-central and mpremote mip install aioble-client

