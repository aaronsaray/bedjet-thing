# ESPHome ESP32 BedJet3 Control

* Connect device
* Visit https://micropython.org/download/ESP32_GENERIC/ and download latest firmware
* `brew install micropython`
* `ls /dev/tty.usb*` to see the usb name
* `esptool.py --port /dev/tty.usbserial-0001 erase_flash`
* `esptool.py --chip esp32 --port /dev/tty.usbserial-0001 --baud 921600 write_flash -z 0x1000 ESP32_GENERIC-20240602-v1.23.0.bin`
* `pipx install rshell`
* `rshell -p /dev/tty.usbserial-0001`
    * `ls` is local directory
    * `ls /pyboard` is the board itself
    * `cp main.py /pyboard`

Restart and it's going to run the code.

You can run the VS Code User Task called Copy to ESP32 which will copy over files and do a soft reset.
