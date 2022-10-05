import random
from machine import Pin, PWM
import utime

def main(): 
    global state
    while True:
        if not on_button.value():
            print("nel")
            put_velocity(0, 0)
            utime.sleep(.1)    
        else:        
            print("osiosi")
            read_values()
            search()
            put_state()
            print(state)
            utime.sleep(.1)
        
def search():
    """Random Search"""
    global state, counter, ground_front, ground_back , last
    if state == 'straight':
        if 0 in ground_front:
            # stop
            put_velocity(0,0)
            utime.sleep(.1)
            counter = 10
            state = "back"
            if ground_front[0] == 0:
                last = "turn_right"
            else:
                last = "turn_left"
    elif state == 'turn_left' or state == "turn_right":
        if counter > 0:
            counter -= 1     
        else:
            state = 'straight'
    elif state == "back":
        if counter > 0:
            counter -= 1                  
        else:
            counter  = 30#random.randint(5, 14)
            state = last

def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def put_velocity(left, right):    
    left_wheel.duty_ns(_map(left,-100,100,2000000,1000000))
    right_wheel.duty_ns(_map(right,-100,100,2000000,1000000))

def put_state():
    """put velocities in one state"""
    if state == "stop":
        put_velocity(0,0)
    elif state == "straight":
        put_velocity(10,10)
    elif state == "turn_left":
        put_velocity(10,-10)
    elif state == "turn_right":
        put_velocity(-10,10)
    elif state == "back":
        put_velocity(10,10)

def read_values():
    read_ground()

def read_ground():
    global ground_front, ground_back, ground
    ground_front[1] = ground[2].value()
    ground_front[0] = ground[3].value()
    ground_back[0] = ground[1].value()
    ground_back[1] = ground[0].value()
    print("ground_front: "+str(ground_front)+"      ground_back: "+str(ground_back))

# Declaration of 4 ground sensors (10,12,14,16)
ground = [Pin(x, Pin.IN) for x in [7,9,10,12]]#1 black 0 blanco
ground_front = [0]*2
ground_back = [0]*2
last = ""
on_button = Pin(4, Pin.IN)

frequency = 300  #10Khz
left_wheel = PWM(Pin(17))
left_wheel.freq(frequency)
right_wheel = PWM(Pin(16))
right_wheel.freq(frequency)
put_velocity(0, 0)

state = 'straight'
counter = 0
start = None

main()