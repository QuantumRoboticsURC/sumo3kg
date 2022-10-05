import random
from machine import Pin, PWM
import utime

last = " "
def main(): 
    global state, ground_back, ground_front, counter, counter_b, last
    global laser_value, lateral, lateral_front, front
    while True:
        if not on_button.value():
            print("nel")
            put_velocity(0, 0)
            utime.sleep(.001)    
        else:        
            print("osiosi")
            read_values()
            
            if 1 in lateral_front:
                if lateral_front[0]:
                    print("Gira Izquierda")
                    put_velocity(20,40)
                    last = "left"
                else:
                    print("Gira derecha")
                    put_velocity(40,20)
                    last = "right"
            elif 1 == front:
                put_velocity(0,0)
            else:
                if last == " ":
                    put_velocity(0,0)
                elif last == "right":
                    put_velocity(40,20)
                elif last == "left":
                    put_velocity(20,40)
                counter_b-=1
                
            
            print(state)
            utime.sleep(.001)

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
        vel = 70
        put_velocity(vel,vel)
    elif state == "turn_left":
        vel = 80
        put_velocity(vel,-vel)
    elif state == "turn_right":
        vel = 80
        put_velocity(-vel,vel)
    elif state == "back":
        vel = -80
        put_velocity(vel,vel)

def read_values():
    #read_ground()
    read_laser()


def read_ground():
    global ground_front, ground_back, ground
    ground_front[1] = ground[2].value()
    ground_front[0] = ground[3].value()
    ground_back[0] = ground[1].value()
    ground_back[1] = ground[0].value()
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

# Declaration of 4 ground sensors (10,12,14,16)
ground = [Pin(x, Pin.IN) for x in [7,9,10,12]]#1 black 0 blanco
ground_front = [1]*2
ground_back = [1]*2
last = ""
on_button = Pin(4, Pin.IN)

# Declaration of 5 laser sensors  (31,32,34,2,5)
laser = [Pin(x, Pin.IN) for x in [26,27,28,1,3]] #1 detecta algo
lateral = [0]*2
lateral_front = [0]*2
front = 0

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