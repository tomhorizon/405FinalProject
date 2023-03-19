import pyb

class GoButton:
    """! @brief GoButton class creates and carries a GoButton object. The user is able to track the value
    of the GoButton (High or Low)
    """
    def __init__(self, pin):
        """! Initialization of a GoButton object. The GPIO pin is initialized in PULL_DOWN mode, meaning the signal
        is normally low, and then turns to high when the button is engaged.
        @param pin: PYB pin number of the GoButton object.
        """
        self.buttonPin = pyb.Pin(pin, pyb.Pin.PULL_DOWN)

    def value(self):
        """! Returns the value of the button's GPIO pin (high or low)
        """
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