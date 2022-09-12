import random

poss_velocities = {"low":0,"medium":15,"high":30}

left_velocity = poss_velocities["medium"]
right_velocity = poss_velocities["medium"]

# Declaration of 3 ground sensors
# Declaration of 6 pwm
# Declaration of 3 laser sensors

state = 'straight'
counter = 0

def main():
    """General execution and planning"""
    configuration()
    while True:
        random_search()

def configuration():
    """Read the buttons to see changes in initial configuration"""
    pass

def search():
    """Pattern to search"""
    pass

def random_search():
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
    change_velocities()

def attack():
    """Search oponent based on laser sensors"""
    pass

def possible_fall():
    """Checks 3 input sensors and change velocity"""
    pass

def change_velocities():
    """Based on left and right velocity, triplicates output"""
    pass

main()