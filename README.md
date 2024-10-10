# ESPHome ESP32 BedJet3 Control

* Connect device
* Visit https://micropython.org/download/ESP32_GENERIC/ and download latest firmware
* `brew install micropython`
* `ls /dev/tty.usb*` to see the usb name
* `esptool.py --port /dev/tty.usbserial-0001 erase_flash`
* `esptool.py --chip esp32 --port /dev/tty.usbserial-0001 write_flash -z 0x1000 ESP32_GENERIC-20240602-v1.23.0.bin`
* `pipx install rshell`

Restart and it's going to run the code.

To deploy a file:

`rshell -p /dev/tty.usbserial-0001 cp boot.py /pyboard`
`rshell -p /dev/tty.usbserial-0001 cp main.py /pyboard`

Rsync the files over:
`rshell -p /dev/tty.usbserial-0001 rsync src /pyboard/src`
`rshell -p /dev/tty.usbserial-0001 rsync web /pyboard/web`

## Functionality

* Loads and blinks blue LED. When connected, turns solid blue for 3 seconds then goes out
* Loads 'bedjet.json' if it exists to connect to wifi network