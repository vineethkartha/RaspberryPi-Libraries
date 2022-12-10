import RPi.GPIO as gpio
from time import sleep

class LedModule:
    anode=0;
    def __init__(self, anode):
        self.anode = anode;
        gpio.setwarnings(True)           
        gpio.setmode(gpio.BCM)
        gpio.setup(anode,gpio.OUT)

    def __del__(self):
        print("Destructor called")
        gpio.output(self.anode, False)
                
    def TurnOn(self):
        gpio.output(self.anode, True)

    def TurnOff(self):
        gpio.output(self.anode, False)

