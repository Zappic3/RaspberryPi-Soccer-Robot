import RPi.GPIO as GPIO
from time import sleep

class Controller:
    def __init__(self, mlf=24, mlb=23, mrf=27, mrb=22, msf=21, msb=20):
        self.mlf = mlf # links vorwärts
        self.mlb = mlb # links rückwärts
        self.mrf = mrf # rechts vorwärts
        self.mrb = mrb # rechts rückwärts
        self.msf = msf # schuss vorwärts
        self.msb = msb  # schuss rückwärts
        self.slow_speed = 100
        
        GPIO.setmode(GPIO.BCM)
        
        # init script
        
        GPIO.setwarnings(False)
        # drive motor pins
        GPIO.setup(self.mlf, GPIO.OUT)
        GPIO.setup(self.mlb, GPIO.OUT)
        GPIO.setup(self.mrf, GPIO.OUT)
        GPIO.setup(self.mrb, GPIO.OUT)
        # shoot motor pins
        GPIO.setup(msf, GPIO.OUT)
        GPIO.setup(msb, GPIO.OUT)
         
        # set PWM frequency
        self.lf_frequency = GPIO.PWM(self.mlf, 100)
        self.lb_frequency = GPIO.PWM(self.mlb, 100)
        self.rf_frequency = GPIO.PWM(self.mrf, 100)
        self.rb_frequency = GPIO.PWM(self.mrb, 100)
        self.shot_frequency_f = GPIO.PWM(self.msf, 50)
        self.shot_frequency_b = GPIO.PWM(self.msb, 50)
        self.status = "idle"
        self.shooting = False
        
        # activate Frequency
        self.lf_frequency.start(0)
        self.lb_frequency.start(0)
        self.rf_frequency.start(0)
        self.rb_frequency.start(0)

    def get_status(self):
        return self.status


    def forward(self):
        self.lf_frequency.ChangeDutyCycle(100)
        self.lb_frequency.ChangeDutyCycle(0)
        self.rf_frequency.ChangeDutyCycle(100)
        self.rb_frequency.ChangeDutyCycle(0)
        self.status = "forward"

    def idle(self):
        self.lf_frequency.ChangeDutyCycle(0)
        self.lb_frequency.ChangeDutyCycle(0)
        self.rf_frequency.ChangeDutyCycle(0)
        self.rb_frequency.ChangeDutyCycle(0)
        self.status = "idle"
    
    def backward(self):
        self.lf_frequency.ChangeDutyCycle(0)
        self.lb_frequency.ChangeDutyCycle(100)
        self.rf_frequency.ChangeDutyCycle(0)
        self.rb_frequency.ChangeDutyCycle(100)
        self.status = "backward"
    
    def spin_r(self):
        self.lf_frequency.ChangeDutyCycle(100)
        self.lb_frequency.ChangeDutyCycle(0)
        self.rf_frequency.ChangeDutyCycle(0)
        self.rb_frequency.ChangeDutyCycle(100)
        self.status = "spin_r"
    
    def spin_l(self):
        self.lf_frequency.ChangeDutyCycle(0)
        self.lb_frequency.ChangeDutyCycle(100)
        self.rf_frequency.ChangeDutyCycle(100)
        self.rb_frequency.ChangeDutyCycle(0)
        self.status = "spin_l"
    
    def turn_l(self):
        self.lf_frequency.ChangeDutyCycle(0)
        self.lb_frequency.ChangeDutyCycle(0)
        self.rf_frequency.ChangeDutyCycle(100)
        self.rb_frequency.ChangeDutyCycle(0)
        self.status = "turn_l" 
    
    def turn_r(self):
        self.lf_frequency.ChangeDutyCycle(100)
        self.lb_frequency.ChangeDutyCycle(0)
        self.rf_frequency.ChangeDutyCycle(0)
        self.rb_frequency.ChangeDutyCycle(0)
        self.status = "turn_r"

    def slow_spin_l(self):
        self.lb_frequency.ChangeDutyCycle(self.slow_speed)
        self.rf_frequency.ChangeDutyCycle(self.slow_speed)
        self.lf_frequency.ChangeDutyCycle(0)
        self.rb_frequency.ChangeDutyCycle(0)

        self.status = "slow_turn_l"

    def slow_spin_r(self):
        self.lb_frequency.ChangeDutyCycle(0)
        self.rf_frequency.ChangeDutyCycle(0)
        self.lf_frequency.ChangeDutyCycle(self.slow_speed)
        self.rb_frequency.ChangeDutyCycle(self.slow_speed)

        self.status = "slow_turn_r"

    def shoot(self, turn_on=False, direction=1):
        if turn_on:
            if direction == 1:
                print(1)
                self.shot_frequency_b.start(50)
                self.shot_frequency_f.stop()
            elif direction == -1:
                print(-1)
                self.shot_frequency_f.start(50)
                self.shot_frequency_b.stop()
        else:
            self.shot_frequency_f.stop()
            self.shot_frequency_b.stop()

#if __name__ == __main__:
    #controller = Controller()
    #controller.spin_l()
    #print(controller.status)
    #sleep(3)
    #controller.slow_spin_r()
    #print(controller.status)
    #sleep(3)
    #controller.turn_r()
    #print(controller.status)
    #sleep(3)
    #controller.turn_l()
    #print(controller.status)
    #sleep(3)
    #controller.spin_l()
    #print(controller.status)
    #sleep(3)
    #controller.spin_r()
    #print(controller.status)
    #sleep(3)
    #controller.backward()
    #print(controller.status)
    #sleep(3)
    #controller.forward()
    #print(controller.status)


