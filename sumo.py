import random
from machine import Pin, PWM
import utime

def main():
    """General execution and planning"""      
    start()  
    while on:
        search()

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
    global state
    global counter        
    if state == 'straight':
        if possible_fall():
            # Change inmediatly
            state = "stop"
            counter  = random.randint(5, 14)
            state = "turn_left"
    elif state == 'turn_left':       
        if counter > 0:
            counter -= 1      
        else:    
            state = 'straight'    
    put_state()

def put_state():
    """put velocities in one state"""
    if state == "stop":
        left_velocity = poss_velocities["medium"]
        right_velocity = poss_velocities["medium"]
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

poss_velocities = {"low":0,"medium":15,"high":30}
left_velocity = poss_velocities["medium"]
right_velocity = poss_velocities["medium"]

# Declaration of 4 ground sensors (10,12,14,16)
ground = [x, Pin.IN) for x in range(10,18,2)]

# Activation
# Declaration of 2 pwm (21,22)
frequency = 1000  #10Khz
left_wheel = PWM(Pin(16))
left_wheel.freq(frequency)
right_wheel = PWM(Pin(17))
right_wheel.freq(frequency)
#led.duty_u16(1)

# Declaration of 5 laser sensors  (31,32,34,2,5)
laser = [Pin(x, Pin.IN) for x in [31,32,34,2,5]]
# Declaration of 4 buttons (24-27)
buttons = [Pin(x, Pin.IN, Pin.PULL_UP) for x in range(24,28)]
on_button = Pin(x, Pin.IN, Pin.PULL_UP) for x in range(24,28)

while on_button.value()!=0:
    utime.sleep(.01)

on = True
state = 'straight'
counter = 0
start = None


configuration()
main()