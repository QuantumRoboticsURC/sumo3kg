import random
from machine import Pin, PWM
import utime

def main():
    while True:        
        #entre 0 y 65535
        left_wheel.duty_u16(1600)
        right_wheel.duty_u16(1600)
        utime.sleep(.1)

# Activation
# Declaration of 2 pwm (21,22)
frequency = 1000  #10Khz
left_wheel = PWM(Pin(16))
left_wheel.freq(frequency)
right_wheel = PWM(Pin(17))
right_wheel.freq(frequency)
#led.duty_u16(1)

main()