import random
from machine import Pin, PWM
import utime

def main(): 
    global state, ground_back, ground_front, counter, counter_b
    global laser_value, lateral, lateral_front, front, last_laser
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
                    vel = 75
                    put_velocity(vel,vel)
                    counter_b = 30
                elif ground_back[0] == 0:
                    print("Gira derecha")
                    put_velocity(75,20)
                    counter_b = 20
                elif ground_back[1] == 0:
                    print("Gira Izquierda")
                    put_velocity(20,75)
                    counter_b = 20
            elif 1 == front:
                #print("frente")
                state = "straight"
                put_state()
                last_laser = " "
            elif 1 in lateral_front:
                if lateral_front[0]:
                    #print("Gira Izquierda")
                    put_velocity(20,75)
                    last_laser = "left"
                else:
                    #print("Gira derecha")
                    put_velocity(75,20)
                    last_laser = "right"
            elif counter_b == 0:
                if last_laser == " ":
                    search()
                    put_state()
                elif last_laser == "right":
                    state = 'straight'
                    put_velocity(75,20)
                elif last_laser == "left":
                    state = 'straight'
                    put_velocity(20,75)
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
            counter = 8
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
            counter  = 11#Turn
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
        vel = 70
        put_velocity(vel,vel)
    elif state == "turn_left":
        vel = 75
        put_velocity(vel,-vel)
    elif state == "turn_right":
        vel = 75
        put_velocity(-vel,vel)
    elif state == "back":
        vel = -70
        put_velocity(vel,vel)

def read_values():
    read_ground()
    read_laser()

def read_ground():
    global ground_front, ground_back, ground
    ground_front[1] = ground[2].value()
    ground_front[0] = ground[3].value()
    ground_back[0] = ground[1].value()
    ground_back[1] = ground[0].value()
    #print("ground_front: "+str(ground_front)+"      ground_back: "+str(ground_back))

def read_laser():    
    global laser_value, lateral, lateral_front, front
    #[31,32,34,2,5]
    lateral[0] = laser[4].value()
    lateral[1] = laser[3].value()
    lateral_front[0] = laser[1].value()
    lateral_front[1] = laser[2].value()
    front = laser[0].value()
    print("lateral: "+str(lateral)+"      lateral_front: "+str(lateral_front)+"       front: "+str(front))

# Declaration of 4 ground sensors (10,12,14,16)
ground = [Pin(x, Pin.IN) for x in [7,9,10,12]]#1 black 0 blanco
ground_front = [0]*2
ground_back = [0]*2
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
last_laser = " "
start = None

main()