import pyb

class GoButton:
    def __init__(self, pin):
        self.buttonPin = pyb.Pin(pin, pyb.Pin.PULL_DOWN)

    def value(self):
        value = self.buttonPin.value()
        return value
    
if __name__ == "__main__":
    goButtonPin = pyb.Pin.board.PA15
    goButton = GoButton(goButtonPin)
    
#     while not goButton.value() == 0:
    while True:
        print(goButton.value())
        pyb.delay(5)
#     print("Go Button Engaged")