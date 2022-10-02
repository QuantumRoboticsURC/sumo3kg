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
    print("ground_front: "+str(ground_front)+"      ground_back: "+str(ground_back))

def read_laser():    
    global laser_value, lateral, lateral_front, front
    #[31,32,34,2,5]
    lateral[0] = laser[3].value()
    lateral[1] = laser[4].value()
    lateral_front[0] = laser[2].value()
    lateral_front[1] = laser[1].value()
    front = laser[0].value()
    print("lateral: "+str(laterakl)+"      lateral_front: "+str(lateral_front)+"       front: "+str(front))

def read_buttons():
    global buttons_value
    for i in range(len(buttons)):
        buttons_value[i] = buttons[i].value()
    print("buttons: "+str(buttons_value))

def read_button():
    print(on_button.value())
    
poss_velocities = {"low":0,"medium":15,"high":30}
left_velocity = poss_velocities["medium"]
right_velocity = poss_velocities["medium"]

# Declaration of 4 ground sensors (10,12,14,16)
ground = [Pin(x, Pin.IN) for x in [7,9,10,12]]
ground_front = [0]*2
ground_back = [0]*2

# Activation
# Declaration of 2 pwm (21,22)
"""frequency = 1000  #10Khz
left_wheel = PWM(Pin(16))
left_wheel.freq(frequency)
right_wheel = PWM(Pin(17))
right_wheel.freq(frequency)"""
#led.duty_u16(1)

# Declaration of 5 laser sensors  (31,32,34,2,5)
laser = [Pin(x, Pin.IN) for x in [26,27,28,1,3]]
lateral = [0]*2, lateral_front = [0]*2, front = 0

# Declaration of 4 buttons (24-27)
buttons = [Pin(x, Pin.IN, Pin.PULL_UP) for x in range(18,22)]
buttons_value = [0]*len(buttons)
on_button = Pin(12, Pin.IN, Pin)

#configuration()
main()