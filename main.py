import random
from machine import Pin, PWM
import utime
from sumo import Sumo

class Strategy():
    def __init__(self):
        self.vel_ini = 80
        self.started = False
        self.sumo = Sumo()
        self.estrategia()

    def estrategia(self):
        while True:
            if not self.sumo.on_button.value() and self.sumo.buttons_value[0] == 0:
                print("nel")
                self.sumo.put_velocity(0, 0)
                self.sumo.read_buttons()
                utime.sleep(.01)
            else:        
                self.sumo.read_values()                        
                if 0 in self.sumo.ground_back:
                    self.started = True
                    self.last_laser = " "
                    if self.sumo.ground_back[0] == 0 and self.sumo.ground_back[1] == 0:
                        self.vel = 75
                        self.sumo.put_velocity(self.vel,self.vel)
                        self.counter_b = 30
                    elif self.sumo.ground_back[0] == 0:
                        self.sumo.put_velocity(75,50)
                        self.counter_b = 20
                    elif ground_back[1] == 0:
                        self.sumo.put_velocity(50,75)
                        self.counter_b = 20
                elif 0 in self.sumo.ground_front:
                    self.started = True
                    self.sumo.last_laser = " "
                    self.search()
                    self.sumo.put_state()
                elif self.state == "back":
                    self.started = True
                    if self.counter > 0:
                        self.counter -= 1                  
                    else:
                        if self.last == "both":
                            self.counter  = 25#Turn
                        else:                
                            self.counter  = 20#Turn
                        self.state = last
                    self.sumo.put_state()   
                elif not started:
                    # Leer segun el boton
                    if self.sumo.buttons_value[1] == 0:
                        if self.sumo.buttons_value[2] == 0:
                            #Frente
                            if self.sumo.buttons_value[3] == 0:
                                # Avanzar recto
                                print("Espalda, girar izquierda")                            
                                self.put_velocity(-self.vel_ini,self.vel_ini)
                                utime.sleep(.2)
                            else:
                                # Avanzar recto (delay)
                                print("Avanzar recto delay")
                                utime.sleep(2)
                                self.sumo.put_velocity(self.vel_ini,self.vel_ini)                            
                        else:
                            # Espalda                        
                            if self.sumo.buttons_value[3] == 0:
                                # Girar Izquierda                            
                                print("Avanzar recto")
                                self.sumo.put_velocity(self.vel_ini,self.vel_ini)
                            else:
                                # Girar Derecha
                                print("Espalda, girar derecha")
                                self.sumo.put_velocity(self.vel_ini,-self.vel_ini)
                    else:                    
                        # Lateral                    
                        if self.sumo.buttons_value[2] == 0:
                            # Girar
                            if self.sumo.buttons_value[3] == 0:
                                print("Lateral girar izquierda")
                                # Izquierda
                                self.sumo.put_velocity(-self.vel_ini,self.vel_ini)
                            else:
                                # Derecha
                                print("Lateral girar derecha")
                                self.sumo.put_velocity(self.vel_ini,-self.vel_ini)
                        else:                        
                            # Avanzar y luego girar
                            if self.sumo.buttons[3] == 0:
                                print("avanzar y luego girar izquierda")
                                # Izquierda
                                self.sumo.put_velocity(40,75)
                                utime.sleep(.2)
                                self.sumo.put_velocity(-self.vel_ini,self.vel_ini)
                            else:
                                # Derecha
                                print("avanzar y luego girar derecha")
                                self.sumo.put_velocity(self.vel_ini,self.vel_ini)
                                utime.sleep(1)
                                self.sumo.put_velocity(self.vel_ini,-self.vel_ini)   
                    self.started = True  
                elif 1 == self.sumo.front:
                    self.started = True
                    self.state = "straight"
                    self.sumo.put_state()
                    self.last_laser = " "
                elif 1 in self.sumo.lateral_front:
                    self.started = True
                    if self.sumo.lateral_front[0]:
                        self.sumo.put_velocity(20,75)
                        self.last_laser = "left"
                    else:
                        self.sumo.put_velocity(75,20)
                        self.last_laser = "right"
                elif 1 in self.sumo.lateral:
                    self.started = True
                    self.state = 'straight'
                    self.vel = 85
                    if self.sumo.lateral[0]:           
                        self.sumo.put_velocity(-self.vel,self.vel)
                        self.last = "left_recio"
                    else:
                        self.sumo.put_velocity(self.vel,-self.vel)
                        self.last = "right_recio"                
                elif self.counter_b == 0:
                    if self.last_laser == " ":
                        self.sumo.search()
                        self.sumo.put_state()
                    elif self.sumo.last_laser == "right":
                        self.state = 'straight'
                        self.sumo.put_velocity(75,20)
                    elif self.last_laser == "left":
                        self.state = 'straight'
                        self.sumo.put_velocity(20,75)
                    elif self.last == "left_recio":
                        self.state = 'straight'
                        self.vel = 85
                        self.sumo.put_velocity(-self.vel,self.vel)
                    elif last == "right_recio":
                        self.vel = 85
                        self.state = 'straight'
                        self.sumo.put_velocity(self.vel,-self.vel)
                else:
                    self.counter_b-=1
                    
                utime.sleep(.01)
        
    def search(self):
        """Random Search"""
        if self.state == 'straight':
            if 0 in self.sumo.ground_front:
                self.counter = 20
                self.state = "back"
                if self.sumo.ground_front[0] == 0 and self.sumo.ground_front[1] == 0:
                    self.last  = "both"
                if self.sumo.ground_front[0] == 0:
                    self.last = "turn_right"
                else:
                    self.last = "turn_left"
        elif self.state == 'turn_left' or self.state == "turn_right":
            if self.counter > 0:
                self.counter -= 1     
            else:
                self.state = 'straight'
        elif self.state == "back":
            if self.counter > 0:
                self.counter -= 1                  
            else:
                if self.last == "both":
                    self.counter = 25#Turn
                else:                
                    self.counter = 20#Turn
                self.state = last
partida = Strategy()