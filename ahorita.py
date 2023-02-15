import random
from machine import Pin, PWM
import utime

def main(): 
    global state, ground_back, ground_front, counter, counter_b, last
    global laser_value, lateral, lateral_front, front, last_laser

    vel_ini = 90
    started = False
    init_time = 1000

    while True:
        if not on_button.value() and buttons_value[0] == 0:
            print("nel")
            put_velocity(0, 0)
            read_buttons()
            utime.sleep(.01)
        else:        
            read_values()
                       
            if 0 in ground_back:
                started = True
                last_laser = " "
                if ground_back[0] == 0 and ground_back[1] == 0:
                    vel = 75
                    put_velocity(vel,vel)
                    counter_b = 30
                elif ground_back[0] == 0:
                    put_velocity(75,50)
                    counter_b = 20
                elif ground_back[1] == 0:
                    put_velocity(50,75)
                    counter_b = 20
            elif 0 in ground_front:
                started = True
                last_laser = " "
                search()
                put_state()
            elif state == "back":
                started = True
                if counter > 0:
                    counter -= 1                  
                else:
                    if last == "both":
                        counter  = 25#Turn
                    else:                
                        counter  = 20#Turn
                    state = last
                put_state()   
            elif not started:
                # Leer segun el boton
                if buttons_value[1] == 0:
                    if buttons_value[2] == 0:
                        if buttons_value[3] == 0:
                            # Avanzar recto
                            print("Espalda, girar izquierda")                            
                            put_velocity(-vel_ini,vel_ini)
                            utime.sleep(.2)                                
                elif buttons_value[1] == 1 and buttons_value[2] == 1 and buttons_value[3] == 0:
                    print("Vuelta abierta")
                    put_velocity(vel_ini,-20)              
                    utime.sleep(.4)
                started = True      
            elif 1 == front:
                started = True
                state = "straight"
                #put_state()
                put_velocity(85,85)
                last_laser = " "
            elif 1 in lateral_front:
                started = True
                if lateral_front[0]:
                    put_velocity(20,80)
                    last_laser = "left"
                else:
                    put_velocity(80,20)
                    last_laser = "right"
            elif 1 in lateral:
                started = True
                state = 'straight'
                vel = 85
                if lateral[0]:           
                    put_velocity(-vel,vel)
                    last = "left_recio"
                else:
                    put_velocity(vel,-vel)
                    last = "right_recio"                
            elif counter_b == 0:
                if last_laser == " ":
                    search()
                    put_state()
                elif last_laser == "right":
                    state = 'straight'
                    put_velocity(80,20)
                elif last_laser == "left":
                    state = 'straight'
                    put_velocity(20,80)
                elif last == "left_recio":
                    state = 'straight'
                    vel = 85
                    put_velocity(-vel,vel)
                elif last == "right_recio":
                    vel = 85
                    state = 'straight'
                    put_velocity(vel,-vel)
            else:
                counter_b-=1
                
            utime.sleep(.01)
        
def search():
    """Random Search"""
    global state, counter, ground_front, ground_back , last
    if state == 'straight':
        if 0 in ground_front:
            counter = 25
            state = "back"
            if ground_front[0] == 0 and ground_front[1] == 0:
                last  = "both"
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
            if last == "both":
                counter  = 25#Turn
            else:                
                counter  = 20#Turn
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
        vel = 80
        put_velocity(-vel,vel)
    elif state == "turn_right":
        vel = 80
        put_velocity(vel,-vel)
    elif state == "back":
        vel = -80
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
    #print("lateral: "+str(lateral)+"      lateral_front: "+str(lateral_front)+"       front: "+str(front))

def read_buttons():
    global buttons_value
    for i in range(len(buttons)):
        buttons_value[i] = buttons[i].value()
    #print("buttons: "+str(buttons_value))

# Declaration of 4 ground sensors (10,12,14,16)
ground = [Pin(x, Pin.IN) for x in [7,9,10,12]]#1 black 0 blanco
ground_front = [0]*2
ground_back = [0]*2
last = ""

# Declaration of 4 buttons (24-27)
buttons = [Pin(x, Pin.IN, Pin.PULL_UP) for x in range(18,22)]
buttons_value = [0]*len(buttons) #0 = on
on_button = Pin(4, Pin.IN) # arriba apagado, abajo prendido 

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

main()
