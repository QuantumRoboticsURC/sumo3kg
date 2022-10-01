import random
from machine import Pin, PWM
import utime

def main():
    while True:
        read_ground()
        utime.sleep(.1)

def read_ground():
    global ground_front, ground_back
    for i in range(2):
        ground_front = ground[i].value()
        ground_back = ground[i+2].value()
    print("front: "+str(ground_front)+"    back"+str(ground_back))

def read_laser():
    global laser_value
    for i in range(len(laser)):
        laser_value[i] = laser[i].value()
    print(laser_value)

def read_buttons():
    global buttons_value
    for i in range(len(buttons)):
        buttons_value[i] = buttons[i].value()
    print(buttons_value)

def read_on_button():
    print(on_button.value())

poss_velocities = {"low":0,"medium":15,"high":30}
left_velocity = poss_velocities["medium"]
right_velocity = poss_velocities["medium"]

# Declaration of 4 ground sensors (10,12,14,16)
ground = [Pin(x, Pin.IN) for x in range(10,18,2)]
ground_front = [0]*2
ground_back = [0]*2

"""# Activation
# Declaration of 2 pwm (21,22)
frequency = 1000  #10Khz
left_wheel = PWM(Pin(16))
left_wheel.freq(frequency)
right_wheel = PWM(Pin(17))
right_wheel.freq(frequency)
#led.duty_u16(1)"""

# Declaration of 5 laser sensors  (31,32,34,2,5)
laser = [Pin(x, Pin.IN) for x in [31,32,34,2,5]]
laser_value = [0]*len(laser)
# Declaration of 4 buttons (24-27)
buttons = [Pin(x, Pin.IN, Pin.PULL_UP) for x in range(24,28)]
buttons_value = [0]*len(buttons)
on_button = Pin(6, Pin.IN, Pin)



#configuration()
main()