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
#import utime as time
from machine import Pin, I2C
from mlx90640 import MLX90640
# from mlx90640 import RefreshRate
from mlx90640.calibration import NUM_ROWS, NUM_COLS, IMAGE_SIZE, TEMP_K
from mlx90640.image import ChessPattern, InterleavedPattern

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


#     def ascii_image(self, array, pixel="██", textcolor="0;180;0"):
#         """!
#         @brief   Show low-resolution camera data as shaded pixels on a text
#                  screen.
#         @details The data is printed as a set of characters in columns for the
#                  number of rows in the camera's image size. This function is
#                  intended for testing an MLX90640 thermal infrared sensor.
# 
#                  A pair of extended ACSII filled rectangles is used by default
#                  to show each pixel so that the aspect ratio of the display on
#                  screens isn't too smushed. Each pixel is colored using ANSI
#                  terminal escape codes which work in only some programs such as
#                  PuTTY.  If shown in simpler terminal programs such as the one
#                  used in Thonny, the display just shows a bunch of pixel
#                  symbols with no difference in shading (boring).
# 
#                  A simple auto-brightness scaling is done, setting the lowest
#                  brightness of a filled block to 0 and the highest to 255. If
#                  there are bad pixels, this can reduce contrast in the rest of
#                  the image.
# 
#                  After the printing is done, character color is reset to a
#                  default of medium-brightness green, or something else if
#                  chosen.
#         @param   array An array of (self._width * self._height) pixel values
#         @param   pixel Text which is shown for each pixel, default being a pair
#                  of extended-ASCII blocks (code 219)
#         @param   textcolor The color to which printed text is reset when the
#                  image has been finished, as a string "<r>;<g>;<b>" with each
#                  letter representing the intensity of red, green, and blue from
#                  0 to 255
#         """
#         minny = min(array)
#         scale = 255.0 / (max(array) - minny)
#         for row in range(self._height):
#             for col in range(self._width):
#                 pix = int((array[row * self._width + (self._width - col - 1)]
#                            - minny) * scale)
#                 print(f"\033[38;2;{pix};{pix};{pix}m{pixel}", end='')
#             print(f"\033[38;2;{textcolor}m")


    ## A "standard" set of characters of different densities to make ASCII art
#     asc = " -.:=+*#%@"


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


#     def get_csv(self, array, limits=None):
#         """!
#         @brief   Generate a string containing image data in CSV format.
#         @details This function generates a set of lines, each having one row of
#                  image data in Comma Separated Variable format. The lines can
#                  be printed or saved to a file using a @c for loop.
#         @param   array The array of data to be presented
#         @param   limits A 2-iterable containing the maximum and minimum values
#                  to which the data should be scaled, or @c None for no scaling
#         """
#         if limits and len(limits) == 2:
#             scale = (limits[1] - limits[0]) / (max(array) - min(array))
#             offset = limits[0] - min(array)
#         else:
#             offset = 0.0
#             scale = 1.0
#         for row in range(self._height):
#             line = ""
#             for col in range(self._width):
#                 pix = int((array[row * self._width + (self._width - col - 1)]
#                           * scale) + offset)
#                 if col:
#                     line += ","
#                 line += f"{pix}"
# #             line += "\r\n"
#             yield line
#         return


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
        for col in range(self._width):
            sum = 0
            for row in range(self._height):
                val = self.pix_map[row][col]
                sum = sum + val
            if sum > sum_old:
                sum_old = sum
                x_target = col
        max_y = 0
        for row in range(self._height):
            if self.pix_map[row][x_target] > max_y:
                max_y = self.pix_map[row][x_target]
                y_target = row
        x_center = self._width/2
        y_center = self._height/2
        
        # Error is computed with relation to the center of the image.
        # A positive error_x --> blaster is aimed too far to the right
        # A positive error_y --> blaster is aimed too high
        error_x = x_center - x_target
        error_y = y_target - y_center
        return error_x, error_y


# def main():
#     
#     KP1 = .1
#             
#     setPoint1 = 5000
#     
#     control1 = Control(KP1, setPoint1 + 32768)
#     
#     print(f'{setPoint1}, {KP1}')
#     encoder1.zero()
#     elapsed = 0
#     startTime = utime.ticks_ms()
#     count = 0
#     while elapsed <= 3000:
#         currentTime = utime.ticks_ms()
#         elapsed = currentTime - startTime
# 
#         pos1 = encoder1.read()
#         print(pos1)
#         psi = control1.run(pos1)
#         motor1.set_duty_cycle(-psi)
#         #print(psi)
#         pyb.delay(10)
#         count += 1
#     
#     print("done")
#     motor1.set_duty_cycle(0)
#     #motor2.set_duty_cycle(0)
#     
#     
#     KP1 = .1
#     setPoint1 = -5000
#     
#     control1 = Control(KP1, setPoint1 + 32768)
#     print(f'{setPoint1}, {KP1}')
#     encoder1.zero()
#     elapsed = 0
#     startTime = utime.ticks_ms()
#     count = 0
#     while elapsed <= 3000:
#         currentTime = utime.ticks_ms()
#         elapsed = currentTime - startTime
# 
#         pos1 = encoder1.read()
#         print(pos1)
#         psi = control1.run(pos1)
#         motor1.set_duty_cycle(-psi)
#         #print(psi)
#         pyb.delay(10)
#         count += 1
#     
#     print("done")
#     motor1.set_duty_cycle(0)
    
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
#     print(gc.mem_free())
    gc.collect()
#     print(gc.mem_free())
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
#         print(camera.target_alg())
        
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
            
            print(psi1, psi2)
        
#         print("done")
        motor1.set_duty_cycle(0)
        motor2.set_duty_cycle(0)
        #motor2.set_duty_cycle(0)
    
    
if __name__ == "__main__":
    loop()
    pyb.delay(10)