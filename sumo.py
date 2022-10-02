import random
from machine import Pin, PWM
import utime

def main():
    """General execution and planning"""      
    start()  
    while on:
        read_values()
        search()
        put_state()
        utime.sleep(.1)

def configuration():
    """Read the buttons to see changes in initial configuration"""
    if buttons[0].value():
        start = start_1()
    else if buttons[1].value():
        start = start_2()

def start_1():
    print("start 1")
    pass

def start_2():
    print("start 2")
    pass

def search():
    """First strategy"""
    global state, counter, ground_front, ground_back 
    if state == 'straight':
        if 1 in ground_front or 1 in ground_back:
            # Change inmediatly
            state = "stop"
            counter  = random.randint(5, 14)
            if ground_front[0]:
                state = "turn_left"
            else:
                state = "turn_right"
    elif state == 'turn_left' or state == "turn_right":
        if counter > 0:
            counter -= 1      
        else:    
            state = 'straight'    

def put_state():
    """put velocities in one state"""
    if state == "stop":
        left_velocity = poss_velocities["low"]
        right_velocity = poss_velocities["low"]
    elif state == "straight":
        left_velocity = poss_velocities["medium"]
        right_velocity = poss_velocities["medium"]
    elif state == "turn_left":
        left_velocity = poss_velocities["high"]
        right_velocity = poss_velocities["medium"]
    else:
        left_velocity = poss_velocities["medium"]
        right_velocity = poss_velocities["high"]

def attack():
    """Search oponent based on laser sensors"""
    pass

def back_off():
    """Checks 3 input sensors and change velocity"""
    pass

def read_values():
    read_ground()

def read_ground():
    global ground_front, ground_back
    for i in range(2):
        ground_front = ground[i].value()
        ground_back = ground[i+2].value()

def read_laser():    
    global laser_value, lateral, lateral_front, front
    #[31,32,34,2,5]
    lateral[0] = laser[3].value()
    lateral[1] = laser[4].value()
    lateral_front[0] = laser[2].value()
    lateral_front[1] = laser[1].value()
    front = laser[0].value()    

def read_buttons():
    global buttons_value
    for i in range(len(buttons)):
        buttons_value[i] = buttons[i].value()

poss_velocities = {"low":0,"medium":15,"high":30}
left_velocity = poss_velocities["medium"]
right_velocity = poss_velocities["medium"]

# Declaration of 4 ground sensors (10,12,14,16)
ground = [Pin(x, Pin.IN) for x in [7,9,10,12]]
ground_front = [0]*2
ground_back = [0]*2

# Activation
# Declaration of 2 pwm (21,22)
frequency = 1000  #10Khz
left_wheel = PWM(Pin(16))
left_wheel.freq(frequency)
right_wheel = PWM(Pin(17))
right_wheel.freq(frequency)
#led.duty_u16(1)

# Declaration of 5 laser sensors  (31,32,34,2,5)
laser = [Pin(x, Pin.IN) for x in [26,27,28,1,3]]
lateral = [0]*2, lateral_front = [0]*2, front = 0

# Declaration of 4 buttons (24-27)
buttons = [Pin(x, Pin.IN, Pin.PULL_UP) for x in range(18,22)]
buttons_value = [0]*len(buttons)
on_button = Pin(12, Pin.IN, Pin)

while on_button.value()!=0:
    utime.sleep(.01)

on = True
state = 'straight'
counter = 0
start = None


#configuration()
main()

