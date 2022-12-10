import RPi.GPIO as gpio

class KeyPadModule:
    mColumnList=[0,0,0,0]
    mRowList = [0,0,0,0]
    key_map=[["1","2","3","bk"],\
             [ "4","5","6","Menu"],\
             [ "7","8","9","Next"],\
             [ "Cancel","0","Enter","Previous"]]
    callbacks=[];

    # The constructor for the class.
    # The arguments are the Rpi Pins corresponding to C1, C2, C3 and C4
    # and theh pins corresponding to R1, R2, R3, R4.
    # we also take in a callback that should be triggered when the button is pressed.
    # The callback should have one argument which will be the 'key' which is pressed.
    def __init__(self,cols,rows, callback=''):
        self.mColumnList = cols
        self.mRowList = rows
        if callback:
            self.callbacks.append(callback)
        gpio.setmode(gpio.BCM)
        for pin in self.mRowList:
            gpio.setup(pin, gpio.OUT)
            gpio.output(pin, gpio.LOW)
        for pin in self.mColumnList:
            gpio.setup(pin, gpio.IN, pull_up_down=gpio.PUD_UP)
            gpio.add_event_detect(pin, gpio.FALLING, callback=self.onKeyPress, bouncetime=200)
        
    def keypadRead(self):
        columnScan=[gpio.input(self.mColumnList[0]),\
                    gpio.input(self.mColumnList[1]),\
                    gpio.input(self.mColumnList[2]),\
                    gpio.input(self.mColumnList[3])]
        colVal=None
        rowVal = None
        if(min(columnScan) == 0):
            colVal=columnScan.index(0);
        if colVal is not None:
            for row in self.mRowList:
                gpio.output(row, gpio.HIGH)
                if gpio.input(self.mColumnList[colVal]) == 1:
                    gpio.output(row, gpio.LOW)
                    rowVal = row
                    break
                gpio.output(row, gpio.LOW)
            if rowVal is not None:
                assert colVal is not None, "Column Value cannot be Null"
                key=self.key_map[int(self.mRowList.index(rowVal))][int(colVal)]
                return(key)

    # this is the callback that will trigger when the button is pressed.
    # The user registered callback will be called from here
    def onKeyPress(self, channel):
        key = self.keypadRead()
        for callback in self.callbacks:
            callback(key)

    def registerCallback(self, callback):
        self.callbacks.append(callback);

    def unregisterCallback(self, callback):
        self.callbacks.remove(callback)
