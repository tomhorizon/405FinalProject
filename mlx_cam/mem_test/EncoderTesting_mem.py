import pyb
import utime as time
import gc
from motor_driver import MotorDriver
from encoder_reader import EncoderReader
from control import Control
#from mlx_cam import MLX_Cam
from machine import Pin, I2C

#Imports for MLX_Cam stuff
# import gc
import array
import uarray
#import utime as time
from machine import Pin, I2C
from mlx90640 import MLX90640
# from mlx90640 import RefreshRate
from mlx90640.calibration import NUM_ROWS, NUM_COLS, IMAGE_SIZE, TEMP_K
from mlx90640.image import ChessPattern, InterleavedPattern

gc.enable()
# motor constants
motor1Pin1 = pyb.Pin.board.PB4
motor1Pin2 = pyb.Pin.board.PB5
motor1Ena = pyb.Pin.board.PA10
motor1Tim = 3
motor1Ch1 = 1
motor1Ch2 = 2

motor2Pin1 = pyb.Pin.board.PA0
motor2Pin2 = pyb.Pin.board.PA1
motor2Ena = pyb.Pin.board.PC1
motor2Tim = 5
motor2Ch1 = 1
motor2Ch2 = 2

# encoder constants
encoder1Pin1 = pyb.Pin.board.PB6
encoder1Pin2 = pyb.Pin.board.PB7
encoder1Tim = 4
encoder1Ch1 = 1
encoder1Ch2 = 2
encoder2Pin1 = pyb.Pin.board.PC6
encoder2Pin2 = pyb.Pin.board.PC7
encoder2Tim = 8
encoder2Ch1 = 1
encoder2Ch2 = 2

# initialize motors and encoder objects
motor1 = MotorDriver(motor1Ena, motor1Pin1, motor1Pin2, motor1Tim, motor1Ch1, motor1Ch2)
motor2 = MotorDriver(motor2Ena, motor2Pin1, motor2Pin2, motor2Tim, motor2Ch1, motor2Ch2)
encoder1 = EncoderReader(encoder1Pin1, encoder1Pin2, encoder1Tim, encoder1Ch1, encoder1Ch2)
encoder2 = EncoderReader(encoder2Pin1, encoder2Pin2, encoder2Tim, encoder2Ch1, encoder2Ch2)

#MLX_CAM stuff
class MLX_Cam:
    """!
    @brief   Class which wraps an MLX90640 thermal infrared camera driver to
             make it easier to grab and use an image.
    """

    def __init__(self, i2c, address=0x33, pattern=ChessPattern,
                 width=NUM_COLS, height=NUM_ROWS):
        """!
        @brief   Set up an MLX90640 camera.
        @param   i2c An I2C bus which has been set up to talk to the camera;
                 this must be a bus object which has already been set up
        @param   address The address of the camera on the I2C bus (default 0x33)
        @param   pattern The way frames are interleaved, as we read only half
                 the pixels at a time (default ChessPattern)
        @param   width The width of the image in pixels; leave it at default
        @param   height The height of the image in pixels; leave it at default
        """
        ## The I2C bus to which the camera is attached
        self._i2c = i2c
        ## The address of the camera on the I2C bus
        self._addr = address
        ## The pattern for reading the camera, usually ChessPattern
        self._pattern = pattern
        ## The width of the image in pixels, which should be 32
        self._width = width
        ## The height of the image in pixels, which should be 24
        self._height = height

        # The MLX90640 object that does the work
        self._camera = MLX90640(i2c, address)
        self._camera.set_pattern(pattern)
        gc.collect()
        self._camera.setup()
        gc.collect()

        ## A local reference to the image object within the camera driver
        self._image = self._camera.image


    def ascii_art(self, array):
        """!
        @brief   Show a data array from the IR image as ASCII art.
        @details Each character is repeated twice so the image isn't squished
                 laterally. A code of "><" indicates an error, probably caused
                 by a bad pixel in the camera. 
        @param   array The array to be shown, probably @c image.v_ir
        """
        asc = " -.:=+*#%@"
        scale = 10 / (max(array) - min(array))
        offset = -min(array)
#         self.pix_map = uarray.create_2d(24, 32, dtype = numpy.uint8)
        self.pix_map = [[0 for j in range(self._width)] for i in range(self._height)]
        for row in range(self._height):
            line = ""
            for col in range(self._width):
                pix = int((array[row * self._width + (self._width - col - 1)]
                           + offset) * scale)
                self.pix_map[row][col] = pix
                try:
#                     the_char = MLX_Cam.asc[pix]
                    the_char = asc[pix]
                    
                    #print(f"{the_char}{the_char}", end='')
                except IndexError: pass
                    #print("><", end='')
            #print('')
        return





    def get_image(self):
        """!
        @brief   Get one image from a MLX90640 camera.
        @details Grab one image from the given camera and return it. Both
                 subframes (the odd checkerboard portions of the image) are
                 grabbed and combined. This assumes that the camera is in the
                 ChessPattern (default) mode as it probably should be.
        @returns A reference to the image object we've just filled with data
        """
        for subpage in (0, 1):
            while not self._camera.has_data:
                time.sleep_ms(50)
#                 print('.', end='')
            self._camera.read_image(subpage)
            state = self._camera.read_state()
            image = self._camera.process_image(subpage, state)

        return image
    
    def target_alg(self):
#         x_sum = array.array('i', self._width*[0])
        sum_old = 0
#         avg_old = 0
        for col in range(31):
            sum = 0
            for row in range(24):
                val = self.pix_map[row][col+1]
#                 if val > 2:
#                     sum = sum + val*val
                sum += val
#             avg = int(sum/32)
#             if avg > avg_old:
#                 avg_old = avg
#                 x_target = col+1
            if sum > sum_old:
                sum_old = sum
                x_target = col+1
        max_y = 0
        for row in range(24):
            if self.pix_map[row][x_target] > max_y:
                max_y = self.pix_map[row][x_target]
                y_target = row
        x_center = self._width/2
        y_center = self._height/2
        
        # Error is computed with relation to the center of the image.
        # A positive error_x --> blaster is aimed too far to the right
        # A positive error_y --> blaster is aimed too high
        #error_x = x_center - x_target
        #error_y = y_target - y_center
        return x_center-x_target, y_target-y_center
    
def loop():
    try:
        from pyb import info

    # Oops, it's not an STM32; assume generic machine.I2C for ESP32 and others
    except ImportError:
        # For ESP32 38-pin cheapo board from NodeMCU, KeeYees, etc.
        i2c_bus = I2C(1, scl=Pin(22), sda=Pin(21))

    # OK, we do have an STM32, so just use the default pin assignments for I2C1
    else:
        i2c_bus = I2C(1)

#     print("MXL90640 Easy(ish) Driver Test")

    # Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33
    scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
#     print(f"I2C Scan: {scanhex}")
    print(gc.mem_free())
    gc.collect()
    print(gc.mem_free())
    camera = MLX_Cam(i2c_bus)
    gc.collect()
    print(gc.mem_free())
    
#     image = camera.get_image()
    KP1 = .15
    
    while True:
        gc.collect()
        image = camera.get_image()
        gc.collect()
        camera.ascii_art(image.v_ir)
        print(camera.target_alg())
        
        Yaw_error, Pitch_error = camera.target_alg()
        
        setPoint1 = Yaw_error*61
        setPoint2 = Pitch_error*61
        control1 = Control(KP1, setPoint1 + 32768)
        control2 = Control(KP1, setPoint2 + 32768)
        
#         print(f'{setPoint1}, {KP1}')
#         print(f'{setPoint2}, {KP1}')
        encoder1.zero()
        encoder2.zero()
        elapsed = 0
        startTime = time.ticks_ms()
        while elapsed <= 1000:
            currentTime = time.ticks_ms()
            elapsed = currentTime - startTime
            pos1 = encoder1.read()
            pos2 = encoder2.read()
            #print(pos1)
            psi1 = control1.run(pos1)
            motor1.set_duty_cycle(-psi1)
            
            pyb.delay(5)
            
            psi2 = control2.run(pos2)
            motor2.set_duty_cycle(-psi2)
            #print(psi)
            pyb.delay(5)
        
#         print("done")
        motor1.set_duty_cycle(0)
        motor2.set_duty_cycle(0)
        #motor2.set_duty_cycle(0)
    
    
if __name__ == "__main__":
    loop()
    pyb.delay(10)