from machine import Pin, PWM

def led_loading():
    status_led_pwm.freq(1)

def led_action():
    status_led_pwm.freq(10)

def led_done():
    status_led_pwm.deinit()

def debug(item):
    print(item)

status_led_pwm = PWM(Pin(2, Pin.OUT))

led_loading()
