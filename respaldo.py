#Biblioteca clásica para raspberry pi pico
import machine
#Genera retardos en el micro
import utime

#Variables
mode = 0
treshold = [24000,24100,24000]  #Sensores de piso


class Motor():
    def __init__(self, IN1, IN2, IN_PWM):
        self.IN1 = machine.Pin(IN1, machine.Pin.OUT)
        self.IN2 = machine.Pin(IN2, machine.Pin.OUT)
        self.PWM = machine.PWM(machine.Pin(IN_PWM))
        self.PWM.freq(100000)
        
    def CCW(self,pwm):
        self.IN1.value(0)
        self.IN2.value(1)
        self.PWM.duty_u16(self.perToDuty(pwm))
        
    def CW(self,pwm):
        self.IN1.value(1)
        self.IN2.value(0)
        self.PWM.duty_u16(self.perToDuty(pwm))
       
    #Freno activo (más fuerte que el pasivo)
    def Stop(self):
        self.IN1.value(0)
        self.IN2.value(0)
        
    def ShortBreak(self):
        self.IN1.value(1)
        self.IN2.value(1)
    
    #Changes pwm percetage to duty cycle for pwm control
    def perToDuty(self,pwm):
        duty_cycle = pwm*65535.0/100.0
        return int(duty_cycle)

class Sumo():
    #SUMO(arrMotor_izq, arrMotor_der,arrayPiso, arrayJS)
    def __init__(self, Mizq, Mder, arrQRT, arrJS, arrControl):
        #Motor(IN1,IN2,PWM)
        self.mDer = Motor(Mder[0],Mder[1],Mder[2])
        self.mIzq = Motor(Mizq[0],Mizq[1],Mizq[2])
        #Sensores de piso
        self.QRTizq = machine.ADC(arrJS[0])
        self.QRTcentral = machine.ADC(arrJS[1])
        self.QRTder = machine.ADC(arrJS[2])
        #Sensores de enemigos
        self.JS40Fizq = machine.Pin(arrJS[0], machine.Pin.IN)
        self.JS40Ffront = machine.Pin(arrJS[1], machine.Pin.IN)
        self.JS40Fder = machine.Pin(arrJS[2], machine.Pin.IN)
        #Control(IN1,IN2,PWM)
        self.READY = machine.Pin(arrControl[0], machine.Pin.IN)
        self.GO = machine.Pin(arrControl[1], machine.Pin.IN)
        self.GO.irq(trigger=machine.Pin.IRQ_RISING , handler=go)
        self.READY.irq(trigger=machine.Pin.IRQ_RISING, handler=modeSelection)
        #Arrays para informacion de escaneos
        self.arrPiso = [0,0,0]   #[IzquierdoFrontal, Derecho Frontal, IzquierdoAtrás, DerechoAtrás]
        self.arrEnemigos = [0,0,0] #[Izquiedo, Frontal, Derecho]
        self.GOstate = 0
        self.READYstate = 0
        
    def avanzar(self,pwm):
        self.mDer.CW(pwm)
        self.mIzq.CW(pwm)
        
    def avanzar2(self,pwmIzq,pwmDer):
        self.mDer.CW(pwmDer)
        self.mIzq.CW(pwmIzq)
        
    def retroceder(self,pwm):
        self.mDer.CCW(pwm)
        self.mIzq.CCW(pwm)
        
    def retroceder2(self,pwmIzq,pwmDer):
        self.mDer.CCW(pwmDer)
        self.mIzq.CCW(pwmIzq)

    def detenerse(self):
        self.mDer.Stop()
        self.mIzq.Stop()
        
    def girarIzq(self,pwm):
         self.mDer.CW(pwm)
         self.mIzq.CCW(pwm)
         
    def girarDer(self,pwm):
         self.mDer.CCW(pwm)
         self.mIzq.CW(pwm)
    
    def readControl(self):
        #self.GOstate = self.GO.value()
        #self.READYstate = self.READY.value()
        return [self.GO.value(),self.READY.value()]
    
    #Lee todos los sensores de piso (B: BACK / F: FRONT)
    def readPiso(self):
        
        global treshold
        #treshold = 24362
        #Escaneo sin delay
        pisoArray = [self.QRTizq.read_u16(), self.QRTcentral.read_u16(), self.QRTder.read_u16()]
        """
        for i in range(len(pisoArray)):
            if pisoArray[i] < treshold[i]:   #Blanco de tectado
                pisoArray[i] = 1
            elif pisoArray[i] >= treshold[i]:
                pisoArray[i] = 0
        """
        #utime.sleep_ms(30)
        return pisoArray
        
    #Escanea con sensores JS40F 
    def readEnemy(self):
        #Escaneo sin delay
        enemyArray = [self.JS40Fizq.value(), self.JS40Ffront.value(), self.JS40Fder.value()]
        #utime.sleep_ms(30)
        return enemyArray
    
    def comprobarDojo(self):
        self.arrPiso = self.readPiso()
        if self.arrPiso[1] == 1:  # Central -> Retrocede
            self.retroceder(100)
            utime.sleep_ms(1000)
            self.giroDer(100)
            utime.sleep_ms(500)
            
        if self.arrPiso[0] == 1:   # Sensores Izq -> gI
            avanzar2(50,100)
            utime.sleep_ms(1000)
            
        if self.arrPiso[2] == 1:   # Sensores 
            avanzar2(100,50)
            utime.sleep_ms(1000)
        
        else:
            self.avanzar2(100,100)
            
    
    def modoBusqueda(self):
        while(True):
            #self.avanzar2(100,40)
            self.girarDer(100)
            self.arrEnemigos = self.readEnemy()
            if ((self.arrEnemigos[0] == 1) or (self.arrEnemigos[1] == 1) or (self.arrEnemigos[2] == 1)):  #Enemigo En frente -> Ataque adelante
                utime.sleep_ms(50)
                break    
            #print(self.READY.value(), self.GO.value())
            if(self.GO.value() == 0) and (self.READY.value() == 0):
                self.detenerse()
                break

            
    def modoFrente(self):
        global treshold
        velRef = 100
        Kp = 15
        scanCounter = 0
        pwmIzq = velRef
        pwmDer = velRef
        
        self.avanzar(100)
        utime.sleep_ms(1750)
            
        self.retroceder(100)
        utime.sleep_ms(1750)
        
        while(True):
            #Leer enemigos
            self.arrEnemigos = self.readEnemy()
            self.arrPiso = self.readPiso()
            print(self.arrEnemigos,self.arrPiso)
            
            #Ataque
            if ((self.arrEnemigos[0] == 1) and (self.arrEnemigos[1] == 1) and (self.arrEnemigos[2] == 1)):  #Enemigo En frente -> Ataque adelante
                pwmIzq = velRef
                pwmDer = velRef
                self.avanzar(velRef)
            else:
                self.modoBusqueda()
                
        
            if(self.GO.value() == 0) and (self.READY.value() == 0):
                self.detenerse()
                break
                #reset()
    def modoAtras(self):
        global treshold
        velRef = 100
        Kp = 15
        scanCounter = 0
        pwmIzq = velRef
        pwmDer = velRef
        
        self.girarDer(100)
        utime.sleep_ms(600)
        
        self.avanzar(100)
        utime.sleep_ms(1750)
            
        self.retroceder(100)
        utime.sleep_ms(1750)
        
        while(True):
            #Leer enemigos
            self.arrEnemigos = self.readEnemy()
            self.arrPiso = self.readPiso()
            print(self.arrEnemigos,self.arrPiso)
            
            #Ataque
            if ((self.arrEnemigos[0] == 1) and (self.arrEnemigos[1] == 1) and (self.arrEnemigos[2] == 1)):  #Enemigo En frente -> Ataque adelante
                pwmIzq = velRef
                pwmDer = velRef
                self.avanzar(velRef)
            else:
                self.modoBusqueda()
                
        
            if(self.GO.value() == 0) and (self.READY.value() == 0):
                self.detenerse()
                break
                #reset()
            
    def modoLadoDer(self):
        global treshold
        velRef = 100
        Kp = 15
        scanCounter = 0
        pwmIzq = velRef
        pwmDer = velRef
        
        self.girarDer(100)
        utime.sleep_ms(300)
        
        self.avanzar(100)
        utime.sleep_ms(1750)
            
        self.retroceder(100)
        utime.sleep_ms(1750)
        
        while(True):
            #Leer enemigos
            self.arrEnemigos = self.readEnemy()
            self.arrPiso = self.readPiso()
            print(self.arrEnemigos,self.arrPiso)
            
            #Ataque
            if ((self.arrEnemigos[0] == 1) and (self.arrEnemigos[1] == 1) and (self.arrEnemigos[2] == 1)):  #Enemigo En frente -> Ataque adelante
                pwmIzq = velRef
                pwmDer = velRef
                self.avanzar(velRef)
            else:
                self.modoBusqueda()
                
        
            if(self.GO.value() == 0) and (self.READY.value() == 0):
                self.detenerse()
                break
                #reset()
            
    def modoLadoIzq(self):
        global treshold
        velRef = 100
        Kp = 15
        scanCounter = 0
        pwmIzq = velRef
        pwmDer = velRef
        
        self.girarIzq(100)
        utime.sleep_ms(300)
        
        self.avanzar(100)
        utime.sleep_ms(1750)
            
        self.retroceder(100)
        utime.sleep_ms(1750)
        
        while(True):
            #Leer enemigos
            self.arrEnemigos = self.readEnemy()
            self.arrPiso = self.readPiso()
            print(self.arrEnemigos,self.arrPiso)
            
            #Ataque
            if ((self.arrEnemigos[0] == 1) and (self.arrEnemigos[1] == 1) and (self.arrEnemigos[2] == 1)):  #Enemigo En frente -> Ataque adelante
                pwmIzq = velRef
                pwmDer = velRef
                self.avanzar(velRef)
            else:
                self.modoBusqueda()
                
        
            if(self.GO.value() == 0) and (self.READY.value() == 0):
                self.detenerse()
                break
                #reset()
    """    
    def modoGiro(self):
        while True:
            self.girarDer(80)
            self.arrEnemigos = self.readEnemy()
            while ((self.arrEnemigos[0] == 1) and (self.arrEnemigos[1] == 1) and (self.arrEnemigos[2] == 1)):
                self.modoAtaque()
                #self.avanzar(100)
                
            if(self.GO.value() == 0) and (self.READY.value() == 0):
                self.detenerse()
                break
            
    def getError(self):
        self.arrEnemigos = self.readEnemy()
        if self.arrEnemigos[0]:
            a = 0
    """
####### PRUEBAS #######

    def pruebaSensoresPiso(self):
        while(True):
            self.arrPiso = self.readPiso()
            print("IZQ: %d  -  CENTRAL: %d  -  DER: %d " % (self.arrPiso[0],self.arrPiso[1],self.arrPiso[2]))
            #print("Izq: %d  -  Central: %d  -  Der: %d" % (self.arrPiso[0],self.arrPiso[1],self.arrPiso[2]))
            utime.sleep_ms(50)
            if(robot.GO.value() == 0) and (robot.READY.value() == 0):
                break
                #reset()
    
    def pruebaSensoresEnemigos(self):
        while(True):
            self.arrEnemigos = self.readEnemy()
            print("Izq: %d  -  Central: %d  -  Der: %d" % (self.arrEnemigos[0],self.arrEnemigos[1],self.arrEnemigos[2]))
            utime.sleep_ms(200)
            
            if(robot.GO.value() == 0) and (robot.READY.value() == 0):
                break
                #reset()
    
####### MODOS #######

####### INTERRUPCIONES #######

def modeSelection(pin):
    global mode
    if mode >= 4:
        mode = 0
    mode += 1
    print("Mode",mode,"selected")

def go(pin):
    global robot
    robot.detenerse()
    if mode == 1:
        print("Modo Frontal")
        robot.modoFrente()
    if mode == 2:
        print("Modo de Espaldas")
        robot.modoAtras()
    if mode == 3:
        print("Modo Lateral")
        robot.modoLadoDer()
    if mode == 4:
        print("Prueba")
        robot.modoLadoIzq()
        
def reset():
    global robot
    robot.detenerse()
        
    
####### Codigo de inicializacion #######

"""
SUMO(Motor_izq, Motor_der, arrPiso, arrJS)
    Motor_izq: [IN1,IN2,PWM]
    Motor_der: [IN1,IN2,PWM]
    Los sensores se declaran de izquierda a derecha priorizando el frente
    arrPiso: Pines de cada sensor x4 en el orden - [Izquierdo, Central, Derecho]
    arrJS: Pines de cada sensor x3 en el orden - [Izquierdo, Frontal, Derecho]
    
"""
robot = Sumo([20,21,22],[19,18,16],[26,27,28],[1,2,0],[15,14]) 

robot.detenerse()


    

