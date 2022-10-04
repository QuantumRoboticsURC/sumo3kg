import random
from machine import Pin, PWM
import utime

def main():
    while True:
        read_button()
        utime.sleep(.1)

def read_ground():
    global ground_front, ground_back, ground
    for i in range(2):
        ground_front[i] = ground[i].value()
        ground_back[i] = ground[i+2].value()
    print("ground_front: "+str(ground_front)+"      ground_back: "+str(ground_back))

def read_laser():    
    global laser_value, lateral, lateral_front, front
    #[31,32,34,2,5]
    lateral[0] = laser[3].value()
    lateral[1] = laser[4].value()
    lateral_front[0] = laser[1].value()
    lateral_front[1] = laser[2].value()
    front = laser[0].value()
    print("lateral: "+str(lateral)+"      lateral_front: "+str(lateral_front)+"       front: "+str(front))

def read_buttons():
    global buttons_value
    for i in range(len(buttons)):
        buttons_value[i] = buttons[i].value()
    print("buttons: "+str(buttons_value))

def read_button():
    print(str(on_button.value()))

# Declaration of 4 ground sensors (10,12,14,16)
"""ground = [Pin(x, Pin.IN) for x in [7,9,10,12]]
ground_front = [0]*2
ground_back = [0]*2"""

# Declaration of 5 laser sensors  (31,32,34,2,5)
"""laser = [Pin(x, Pin.IN) for x in [26,27,28,1,3]]
lateral = [0]*2
lateral_front = [0]*2
front = 0"""

# Declaration of 4 buttons (24-27)
"""buttons = [Pin(x, Pin.IN, Pin.PULL_UP) for x in range(18,22)]
buttons_value = [0]*len(buttons)"""
on_button = Pin(4, Pin.IN)

#configuration()
main()