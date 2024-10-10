from machine import Pin, PWM

class StatusLEDPWM:

    def __init__(self):
        self.led = PWM(Pin(2, Pin.OUT))

    def loading(self):
        self.led.freq(1)

    def action(self):
        self.led.freq(10)

    def done(self):
        self.led.deinit()
