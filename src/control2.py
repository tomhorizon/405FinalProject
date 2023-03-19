import utime as time

class Control2:
    """! @brief The Control class carries out the the calculations for a PID controller based off of Kp, Ki, and Kd,
    and the set point (goal), and the current position
    """
    def __init__(self, kp, ki, kd, setpt):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpt = setpt
        
        self.I = 0
        self.error_prev = 0
        self.t_prev = time.ticks_ms()
        """! Initialization takes in the controller parameters and intiallizes the controller object
        @param kp: Kp is the proportional controller constant (must range from 0 --> 4 for this application)
        @param ki: Ki is the integral controller constant
        @param kd: Kd is the derivative controller constant
        @param setpt: setpt is the setpoint, or the encoder value for the "goal" position of the motor
        """

    def run(self, pos):
        """! The run method takes in the current motor position and calculates and scales the error to ouput the
            necessary motor effort for a PID controller.
        @param pos: pos is the current motor position as read by the encoder
        """
        # Calculate positional error
        self.error = self.setpt - pos
        self.t = time.ticks_ms()
        
        # Perform PID control and configure P,I, and D outputs
        self.psiP = self.kp*self.error
        self.psiI = self.I + self.ki*self.error*(self.t - self.t_prev)
        self.psiD = self.kd*(self.error - self.error_prev)/(self.t - self.t_prev)
        self.psi = self.psiP + self.psiI + self.psiD
        
        #print(f"error: {self.error:.2f}\teffort: {self.psi:.2f}\tP: {self.psiP:.2f}\tI: {self.psiI:.2f}\tD: {self.psiD:.2f}")
        
        self.error_prev = self.error
        self.t_prev = self.t
        
        
        return self.psi
        

    def set_setpoint(self, setpt_new):
        """! set_setpoint takes in the new setpoint, or goal position, of the motor and applies it to the controller object
        @param setpt_new: setpt_new is the new setpoint for the motor, given in an encoder position
        """
        self.setpt = setpt_new
        self.I = 0
        self.t = time.ticks_ms()
        return self.setpt

    def set_Kp(self, kp_new):
        """! set_Kp takes in the new Kp, proortional controller constant, and applies it to the controller object
        @param kp_new: kp_new is the new Kp
        """
        self.kp = kp_new
        print('kp is:', self.kp)
        return self.kp
    
if __name__ == '__main__':
    con = Control2(.15, .15, .15, 1000)