import random
from machine import Pin, PWM
import utime

def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def main():
    while True:        
        per_izq = _map(0,-100,100,2000000,1000000)
        #1500*1000#1600 atras 1400 adelante, 1500 stop
        per_der = _map(0,-100,100,2000000,1000000)
        left_wheel.duty_ns(per_der)
        right_wheel.duty_ns(per_izq)
        #utime.sleep(.1)

# Activation
# Declaration of 2 pwm (21,22)
frequency = 300  #10Khz
left_wheel = PWM(Pin(17))
left_wheel.freq(frequency)
right_wheel = PWM(Pin(16))
right_wheel.freq(frequency)


main()