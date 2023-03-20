import pyb

# IF YOU ARE PLANNING ON TESTING MOTORS, UNPLUG THE ONES NOT USED

class MotorDriver2:
    """!
    @brief   The DC motor is powered by an external 12V supply. The STM32 provides a PWM
             signal that is then turned into -12 to +12V.
    """
    def __init__(self, in1, in2, en_pin, timer_num, timerCh1):
        """! The initialization sets up the output pins and PWM channel.
        @param in1pin: Channel 1 on pin 1 is used for PWM forward.
        @param in2pin: Channel 2 on pin 2 is used for PWM reverse.
        @param en_pin: The motor must be enabled to run. This is done by pulling an input
        pin high - this convention is used so the motor can shut itself off if there
        is an internal fault detected. The input pin will convey the news to the MCU.
        @param timer: The motor receives a functioning timer channel to use.
        """
        self.enapin = pyb.Pin(en_pin, pyb.Pin.OUT_PP)
        self.in1pin = pyb.Pin(in1, pyb.Pin.OUT_PP)
        self.in2pin = pyb.Pin(in2, pyb.Pin.OUT_PP)
        self.timer = pyb.Timer(timer_num, freq=500)
        self.ch1 = self.timer.channel(timerCh1, pyb.Timer.PWM, pin=self.enapin)
        #print("Creating a motor driver")

    def set_duty_cycle(self, input):
        """! The motor will update with a new speed request from -100 to 100 percent. The new
        speed will be printed.
        @param level: Level is the requested speed and direction.
        """
        
        if input <= 0:
            self.level = -1 * input
            self.ch1.pulse_width_percent(self.level)
            self.in1pin.value(1)
            self.in2pin.value(0)
        else:
            self.level = input
            self.ch1.pulse_width_percent(self.level)
            self.in1pin.value(0)
            self.in2pin.value(1)

if __name__ == '__main__':
    import time

    input1Pin = pyb.Pin.board.PC5
    input2Pin = pyb.Pin.board.PB8
    enablePin = pyb.Pin.board.PC8
    motorTimer = 3
    motorChannel = 3
    motor1 = MotorDriver2(input1Pin, input2Pin, enablePin, motorTimer, motorChannel)
    while 1:
        motor1.set_duty_cycle(int(input("Level: ")))
        
