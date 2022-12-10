import RPi.GPIO as gpio
import time

class Servo:
       servoPin=18
       delay=0.01
       freq = 50
       servoMotor='';
       minDutyCycle = 2;
       maxDutyCycle = 11;
       def __init__(self,servoPin,delay=0.01, freq=50, minDutyCycle=2, maxDutyCycle=11):
              self.servoPin = servoPin
              self.delay = delay
              self.freq = freq
              self.minDutyCycle=minDutyCycle
              self.maxDutyCycle=maxDutyCycle
              gpio.setmode(gpio.BCM)
              gpio.setup(self.servoPin,gpio.OUT)
              self.servoMotor=gpio.PWM(self.servoPin,self.freq)# 50hz frequency
       def findDutyCycleForAngle(self,angle):
              dutyCycle = (self.maxDutyCycle-self.minDutyCycle)/180.0 *angle + self.minDutyCycle
              return dutyCycle
       def start(self,angle):
              self.servoMotor.start(self.findDutyCycleForAngle(angle))
       def stop(self):
              self.servoMotor.stop()
       def moveToAngle(self,angle):
              self.servoMotor.ChangeDutyCycle(self.findDutyCycleForAngle(angle))
              time.sleep(self.delay)
              
