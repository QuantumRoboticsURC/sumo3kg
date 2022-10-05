import random
from machine import Pin, PWM
import utime

def main(): 
    while True:
        if not on_button.value():
            print("nel")
            put_velocity(0, 0)
            utime.sleep(.1)    
        else:        
            print("osiosi")
            put_velocity(10, 10)
            utime.sleep(.1)
        
def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def put_velocity(left, right):    
    left_wheel.duty_ns(_map(left,-100,100,2000000,1000000))
    right_wheel.duty_ns(_map(right,-100,100,2000000,1000000))

on_button = Pin(4, Pin.IN)

frequency = 300  #10Khz
left_wheel = PWM(Pin(17))
left_wheel.freq(frequency)
right_wheel = PWM(Pin(16))
right_wheel.freq(frequency)
put_velocity(0, 0)

main()