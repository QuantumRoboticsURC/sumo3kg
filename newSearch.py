import random
from machine import Pin, PWM
import utime

def main(): 
    global state, ground_back, ground_front, counter, counter_b
    while True:
        if not on_button.value():
            print("nel")
            put_velocity(0, 0)
            utime.sleep(.001)    
        else:        
            print("osiosi")
            read_values()
            
            if 0 in ground_front:
                search()
                put_state()
            elif 0 in ground_back:
                if ground_back[0] and ground_back[1]:
                    print("rapidismo al frente")
                    put_velocity(20,20)
                    counter_b = 100
                elif ground_back[0]:
                    print("Gira izquierda")
                    put_velocity(10,20)
                    counter_b = 100
                else:
                    print("Gira Derecha")
                    put_velocity(20,10)
                    counter_b = 100
            elif counter_b == 0:
                search()
                put_state()
            else:
                print("Atras")
                counter_b-=1
                
            
            print(state)
            utime.sleep(.001)
        
def search():
    """Random Search"""
    global state, counter, ground_front, ground_back , last
    if state == 'straight':
        if 0 in ground_front:
            counter = 125
            state = "back"
            if ground_front[0] == 0:
                last = "turn_left"
            else:
                last = "turn_right"
    elif state == 'turn_left' or state == "turn_right":
        if counter > 0:
            counter -= 1     
        else:
            state = 'straight'
    elif state == "back":
        if counter > 0:
            counter -= 1                  
        else:
            counter  = 50#Turn
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
        vel = 80
        put_velocity(vel,vel)
    elif state == "turn_left":
        vel = 100
        put_velocity(vel,-vel)
    elif state == "turn_right":
        vel = 100
        put_velocity(-vel,vel)
    elif state == "back":
        vel = -100
        put_velocity(vel,vel)

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
counter_b = 0
start = None

main()