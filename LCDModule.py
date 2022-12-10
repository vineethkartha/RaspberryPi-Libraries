# Pinout of the LCD:
# 1 : GND
# 2 : 5V power
# 3 : Display contrast - Connect to middle pin potentiometer 
# 4 : RS (Register Select)
# 5 : R/W (Read Write) - Ground this pin (important)
# 6 : Enable or Strobe
# 7 : Data Bit 0 - data pin 0, 1, 2, 3 are not used
# 8 : Data Bit 1 - 
# 9 : Data Bit 2 - 
# 10: Data Bit 3 - 
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V
# 16: LCD Backlight GND

import RPi.GPIO as gpio
import time

# Device constants
LCD_CHR = True # Character mode
LCD_CMD = False # Command mode
LCD_CHARS = 16 # Characters per line (16 max)
LCD_LINE_1 = 0x80 # LCD memory location for 1st line
LCD_LINE_2 = 0xC0 # LCD memory location 2nd line

class LCDModule:
    # GPIO to LCD mapping
    Rs = 0
    En = 0
    d4 = 0
    d5 = 0
    d6 = 0
    d7 = 0
    ledPin = 0
    def __init__(self, RsPin, EnablePin, dataPinList, led):
        gpio.setwarnings(False)
        self.d4=dataPinList[0]
        self.d5=dataPinList[1]
        self.d6=dataPinList[2]
        self.d7=dataPinList[3]
        self.Rs = RsPin
        self.En = EnablePin
        self.ledPin = led
        gpio.setmode(gpio.BCM) # Use BCM GPIO numbers
        gpio.setup(self.En, gpio.OUT) # Set GPIO's to output mode
        gpio.setup(self.Rs, gpio.OUT)
        gpio.setup(self.d4, gpio.OUT)
        gpio.setup(self.d5, gpio.OUT)
        gpio.setup(self.d6, gpio.OUT)
        gpio.setup(self.d7, gpio.OUT)
        gpio.setup(self.ledPin, gpio.OUT)
        gpio.output(self.ledPin, False)
        self.lcdWrite(0x33,LCD_CMD) # Initialize
        self.lcdWrite(0x32,LCD_CMD) # Set to 4-bit mode
        self.lcdWrite(0x06,LCD_CMD) # Cursor move direction
        self.lcdWrite(0x0C,LCD_CMD) # Turn cursor off
        self.lcdWrite(0x28,LCD_CMD) # 2 line display
        self.lcdWrite(0x01,LCD_CMD) # Clear display
        time.sleep(0.0005) # Delay to allow commands to process

    def __del__(self):
        gpio.cleanup()
        
    def lcdWrite(self, bits, mode):
        # High bits
        gpio.output(self.Rs, mode) # RS
        gpio.output(self.d4, False)
        gpio.output(self.d5, False)
        gpio.output(self.d6, False)
        gpio.output(self.d7, False)
        if bits&0x10==0x10:
            gpio.output(self.d4, True)
        if bits&0x20==0x20:
            gpio.output(self.d5, True)
        if bits&0x40==0x40:
            gpio.output(self.d6, True)
        if bits&0x80==0x80:
            gpio.output(self.d7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

        # Low bits
        gpio.output(self.d4, False)
        gpio.output(self.d5, False)
        gpio.output(self.d6, False)
        gpio.output(self.d7, False)
        if bits&0x01==0x01:
            gpio.output(self.d4, True)
        if bits&0x02==0x02:
            gpio.output(self.d5, True)
        if bits&0x04==0x04:
            gpio.output(self.d6, True)
        if bits&0x08==0x08:
            gpio.output(self.d7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

    def lcd_toggle_enable(self):
        time.sleep(0.0005)
        gpio.output(self.En, True)
        time.sleep(0.0005)
        gpio.output(self.En, False)
        time.sleep(0.0005)

    def lcd_text(self, message,line):
        # Send text to display
        message = message.ljust(LCD_CHARS," ")
        self.lcdWrite(line, LCD_CMD)
        for i in range(LCD_CHARS):
            self.lcdWrite(ord(message[i]),LCD_CHR)

    def turnONLed(self, sec):
        gpio.output(self.ledPin, True)
        time.sleep(sec)
        gpio.output(self.ledPin, False)

# Loop - send text and sleep 3 seconds between texts
# Change text to anything you wish, but must be 16 characters or less
#lcdObj = LCDModule(27,22,[2,3,4,17], 14)
#lcdObj.turnONLed(2)
#while True:
#    lcdObj.lcd_text("Raspberry Pi ",LCD_LINE_1)
#    lcdObj.lcd_text("Ready to boot",LCD_LINE_2)
#    time.sleep(3) # 3 second delay
#    lcdObj.lcd_text("Connect via ssh",LCD_LINE_1)
#    lcdObj.lcd_text("pi@raspberrypi.local",LCD_LINE_2)
#    time.sleep(2)
    
