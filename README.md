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

Install mpremote with `pipx install mpremote`

Then, `mpremote mip install aioble-central` and `mpremote mip install aioble-client`

## Shell

`rshell -p /dev/tty.usbserial-0001 repl`

## Visit site on default

http://192.168.4.1

## Development Notes / Notes to Self

### Remaining Tasks

- [ ] Figure out why it crashes after the await for BT provision
- [ ] BT Functionality connect on load (double await - same issue as above?)
- [ ] Configure API end points to control fan when toggled
- [ ] Configure this in homekit
- [ ] Create demo

### References

```
class mode:
	off = 0x01
	cool = 0x02
	heat = 0x03
	turbo = 0x04
	dry = 0x05
	ext_ht = 0x06
	
class control:
	fan_up = 0x10
	fan_down = 0x11
	temp_up = 0x12
	temp_down = 0x13
	
class preset:
	m1 = 0x20
	m2 = 0x21
	m3 = 0x22

self.devname = self.device.char_read("00002001-bed0-0080-aa55-4265644a6574").decode()
		self.device.subscribe("00002000-bed0-0080-aa55-4265644a6574", callback=self.handle_data)


ef handle_data(self, handle, value):
		self.temp_actual = round(((int(value[7]) - 0x26) + 66) - ((int(value[7]) - 0x26) / 9))
		self.temp_setpoint = round(((int(value[8]) - 0x26) + 66) - ((int(value[8]) - 0x26) / 9))
		self.time = (int(value[4]) * 60 *60) + (int(value[5]) * 60) + int(value[6])
		self.timestring = str(int(value[4])) + ":" + str(int(value[5])) + ":" + str(int(value[6]))
		self.fan = int(value[10]) * 5
		if value[14] == 0x50 and value[13] == 0x14:
			self.mode = "off"
		if value[14] == 0x34:
			self.mode = "cool"
		if value[14] == 0x56:
			self.mode = "turbo"
		if value[14] == 0x50 and value[13] == 0x2d:
			self.mode = "heat"
		if value[14] == 0x3e:
			self.mode = "dry"
		if value[14] == 0x43:
			self.mode = "ext ht"
		client.publish("bedjet/" + self.devname + "/temp_actual", self.temp_actual)
		client.publish("bedjet/" + self.devname + "/temp_setpoint", self.temp_setpoint)
		client.publish("bedjet/" + self.devname + "/time", self.time)
		client.publish("bedjet/" + self.devname + "/timestring", self.timestring)
		client.publish("bedjet/" + self.devname + "/fan", self.fan)
		client.publish("bedjet/" + self.devname + "/mode", self.mode)
	
	def set_mode(self, mode):
		self.device.char_write( '00002004-bed0-0080-aa55-4265644a6574', [0x01,mode])
		
	def press_control(self, control):
		self.device.char_write( '00002004-bed0-0080-aa55-4265644a6574', [0x01,control])
		
	def press_preset(self, preset):
		self.device.char_write( '00002004-bed0-0080-aa55-4265644a6574', [0x01,preset])

	def set_fan(self, fanPercent):
		if fanPercent >= 5 and fanPercent <= 100:
			self.device.char_write( '00002004-bed0-0080-aa55-4265644a6574', [0x07,round(fanPercent/5)-1])
		
	def set_temp(self, temp):
		if temp >= 66 and temp <= 104:
			temp_byte = ( int((temp - 60) / 9) + (temp - 66))  + 0x26
			self.device.char_write( '00002004-bed0-0080-aa55-4265644a6574', [0x03,temp_byte])
		
	def set_time(self, minutes):
		self.device.char_write( '00002004-bed0-0080-aa55-4265644a6574', [0x02, minutes // 60, minutes % 60])
```

Some nice reference: https://github.com/asheliahut/ha-bedjet/blob/main/custom_components/bedjet/climate.py

