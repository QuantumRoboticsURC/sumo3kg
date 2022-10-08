import random
from machine import Pin, PWM
import utime

def main(): 
    global state, ground_back, ground_front, counter, counter_b
    while True:
        if not on_button.value():
            print("nel")
            put_velocity(0, 0)
            utime.sleep(.01)    
        else:        
            read_values()
            
            if 0 in ground_front:
                search()
                put_state()
            elif 0 in ground_back:
                #print(ground_back)
                if ground_back[0] == 0 and ground_back[1] == 0:
                    print("rapidismo al frente")
                    vel = 50
                    put_velocity(vel,vel)
                    counter_b = 30
                elif ground_back[0] == 0:
                    print("Gira derecha")
                    vel = 50
                    put_velocity(vel,-vel)
                    #put_velocity(80,60)
                    counter_b = 15
                elif ground_back[1] == 0:
                    print("Gira Izquierda")
                    vel = 50
                    put_velocity(-vel,vel)
                    counter_b = 15
            elif counter_b == 0:
                search()
                put_state()
            else:
                print("Atras")
                counter_b-=1
                
            #print(state)
            utime.sleep(.01)
        
def search():
    """Random Search"""
    global state, counter, ground_front, ground_back , last
    if state == 'straight':
        if 0 in ground_front:
            state = "back"
            utime.sleep(.16)
            put_state()
            if ground_front[0] == 0 and ground_front[1] == 0:
                state = "turn_left"
                counter = 22      
            elif ground_front[0] == 0:
                state = "turn_left"
                counter = 24
            else:
                state = "turn_right"
                counter = 24
    elif state == 'turn_left' or state == "turn_right":
        if counter > 0:
            counter -= 1     
        else:
            state = 'straight'

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
        vel = 50
        put_velocity(vel,vel)
    elif state == "turn_left":
        vel = 50
        put_velocity(vel,-vel)
    elif state == "turn_right":
        vel = 50
        put_velocity(-vel,vel)
    elif state == "back":
        vel = -50
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