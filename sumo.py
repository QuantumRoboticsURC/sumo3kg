import random
from machine import Pin, PWM
import utime


class Sumo():
    def __init__(self):
        # Declaration of 4 ground sensors (10,12,14,16)
        self.ground = [Pin(x, Pin.IN) for x in [7,9,10,12]]#1 black 0 blanco
        self.ground_front = [0]*2
        self.ground_back = [0]*2
        self.last = ""

        # Declaration of 4 buttons (24-27)
        self.buttons = [Pin(x, Pin.IN, Pin.PULL_UP) for x in range(18,22)]
        self.buttons_value = [0]*len(buttons) #0 = on
        self.on_button = Pin(4, Pin.IN) # arriba apagado, abajo prendido 

        # Declaration of 5 laser sensors  (31,32,34,2,5)
        self.laser = [Pin(x, Pin.IN) for x in [26,27,28,1,3]] #1 detecta algo
        self.lateral = [0]*2
        self.lateral_front = [0]*2
        self.front = 0

        #PWM
        self.frequency = 300  #10Khz
        self.left_wheel = PWM(Pin(17))
        self.left_wheel.freq(frequency)
        self.right_wheel = PWM(Pin(16))
        self.right_wheel.freq(frequency)
        self.put_velocity(0, 0)

        self.state = 'straight'
        self.counter = 0
        self.counter_b = 0
        self.last_laser = " "

    def read_values(self):
        read_ground()
        read_laser()

    def read_ground(self):
        self.ground_front[1] = self.ground[2].value()
        self.ground_front[0] = self.ground[3].value()
        self.ground_back[0] = self.ground[1].value()
        self.ground_back[1] = self.ground[0].value()
        #print("ground_front: "+str(ground_front)+"      ground_back: "+str(ground_back))

    def read_laser(self):
        #[31,32,34,2,5]
        self.lateral[0] = self.laser[4].value()
        self.lateral[1] = self.laser[3].value()
        self.lateral_front[0] = self.laser[1].value()
        self.lateral_front[1] = self.laser[2].value()
        self.front = self.laser[0].value()
        #print("lateral: "+str(lateral)+"      lateral_front: "+str(lateral_front)+"       front: "+str(front))

    def read_buttons(self):
        for i in range(len(buttons)):
            self.buttons_value[i] = self.buttons[i].value()
        #print("buttons: "+str(buttons_value))
    
    def _map(self,x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def put_velocity(self, left, right):    
        self.left_wheel.duty_ns(_map(left,-100,100,2000000,1000000))
        self.right_wheel.duty_ns(_map(right,-100,100,2000000,1000000))

    def put_state(self):
        """put velocities in one state"""
        if state == "stop":
            self.put_velocity(0,0)
        elif state == "straight":
            vel = 70
            self.put_velocity(vel,vel)
        elif state == "turn_left":
            vel = 75
            self.put_velocity(-vel,vel)
        elif state == "turn_right":
            vel = 75
            self.put_velocity(vel,-vel)
        elif state == "back":
            vel = -70
            self.put_velocity(vel,vel)

    def test_sensors(self):
        while True:        
            self.read_values()
            utime.sleep(.5)

    def test_pwm(self):
        while True:        
            for i in range(50,90,10):
                print(i)
                per_ = self._map(i,-100,100,2000000,1000000)
                self.left_wheel.dutzy_ns(per_)
                self.right_wheel.dutzy_ns(per_)
                utime.sleep(10)