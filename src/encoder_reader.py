import pyb


class EncoderReader:
    """! @brief The encoder is built into the DC motor. A quadrature
    encoder uses two channels to capture changes in position.
    """

    def __init__(self, pn1, pn2, timer_num, chan1, chan2):
        """! Initialization takes in the pins and sets the initial position to a
        received value.
        @param pin1: Pin 1 is used for encoder channel A.
        @param pin2: Pin 2 is used for encoder channel B.
        @param position: Position is send to the encoder for reference.
        @param old_count: The previous count is compared for overflow correction.
        """
        self.pin1 = pyb.Pin(pn1, pyb.Pin.IN)
        self.pin2 = pyb.Pin(pn2, pyb.Pin.IN)
        self.timer = pyb.Timer(timer_num, prescaler=0, period=0xFFFF)
        self.ch1 = self.timer.channel(chan1, pyb.Timer.ENC_AB, pin=self.pin1)
        self.ch2 = self.timer.channel(chan2, pyb.Timer.ENC_AB, pin=self.pin2)

    def read(self):
        """! This function returns the position of the motor when called.
        It calls the STM32 timer that has been incrementing with every
        encoder signal. Limited by 16 bits, the encoder will overflow back
        to zero or, if moving backwards, underflow to the max value
        again.
        
        @returns counter: returns encoder value
        """
        counter = self.timer.counter()

        return counter

    def zero(self):
        """! The count can be manually reset to zero when starting a new measurement.
        """
        self.timer.counter(32768)


if __name__ == '__main__':
    encoder1Tim = 4
    encoder1Ch1 = 1
    encoder1Ch2 = 2
    p1 = pyb.Pin.board.PB6
    p2 = pyb.Pin.board.PB7
    enc = EncoderReader(p1, p2, encoder1Tim, encoder1Ch1, encoder1Ch2)
    enc.zero()
    while True:
        pos = enc.read()
        print(pos)
#         if enc.timer.counter() > 40000:
#             #print('reset')
#             enc.zero()
        pyb.delay(100)
