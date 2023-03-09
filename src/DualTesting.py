# First Dual Testing File
import pyb
import utime as time
import gc
gc.collect()
from motor_driver2 import MotorDriver2
from encoder_reader import EncoderReader
from control import Control
from machine import Pin, I2C
import array
from mlx90640 import MLX90640
from mlx90640.calibration import NUM_ROWS, NUM_COLS, IMAGE_SIZE, TEMP_K
from mlx90640.image import ChessPattern, InterleavedPattern
from mlx_cam import MLX_Cam
gc.collect()
# motor constants
motor1Pin1 = pyb.Pin.board.PB5
motor1Pin2 = pyb.Pin.board.PA10
motor1Ena = pyb.Pin.board.PB3
motor1Tim = 2
motor1Ch1 = 2

motor2Pin1 = pyb.Pin.board.PA1
motor2Pin2 = pyb.Pin.board.PC1
motor2Ena = pyb.Pin.board.PA0
motor2Tim = 5
motor2Ch1 = 1

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
gc.collect()
# initialize motors and encoder objects
#Motor 1 = Yaw. Motor 2 = Pitch
motor1 = MotorDriver2(motor1Pin1, motor1Pin2, motor1Ena, motor1Tim, motor1Ch1)
motor2 = MotorDriver2(motor2Pin1, motor2Pin2, motor2Ena, motor2Tim, motor2Ch1)
encoder1 = EncoderReader(encoder1Pin1, encoder1Pin2, encoder1Tim, encoder1Ch1, encoder1Ch2)
encoder2 = EncoderReader(encoder2Pin1, encoder2Pin2, encoder2Tim, encoder2Ch1, encoder2Ch2)
gc.collect()
#MLX_CAM stuff
# class MLX_Cam:
#     """!
#     @brief   Class which wraps an MLX90640 thermal infrared camera driver to
#              make it easier to grab and use an image.
#     """
# 
#     def __init__(self, i2c, address=0x33, pattern=ChessPattern,
#                  width=NUM_COLS, height=NUM_ROWS):
#         """!
#         @brief   Set up an MLX90640 camera.
#         @param   i2c An I2C bus which has been set up to talk to the camera;
#                  this must be a bus object which has already been set up
#         @param   address The address of the camera on the I2C bus (default 0x33)
#         @param   pattern The way frames are interleaved, as we read only half
#                  the pixels at a time (default ChessPattern)
#         @param   width The width of the image in pixels; leave it at default
#         @param   height The height of the image in pixels; leave it at default
#         """
#         ## The I2C bus to which the camera is attached
#         self._i2c = i2c
#         ## The address of the camera on the I2C bus
#         self._addr = address
#         ## The pattern for reading the camera, usually ChessPattern
#         self._pattern = pattern
#         ## The width of the image in pixels, which should be 32
#         self._width = width
#         ## The height of the image in pixels, which should be 24
#         self._height = height
#         # The MLX90640 object that does the work
#         self._camera = MLX90640(i2c, address)
#         self._camera.set_pattern(pattern)
#         gc.collect()
#         self._camera.setup()
#         gc.collect()
# 
#         ## A local reference to the image object within the camera driver
#         self._image = self._camera.image
# 
#     def ascii_art(self, array):
#         """!
#         @brief   Show a data array from the IR image as ASCII art.
#         @details Each character is repeated twice so the image isn't squished
#                  laterally. A code of "><" indicates an error, probably caused
#                  by a bad pixel in the camera. 
#         @param   array The array to be shown, probably @c image.v_ir
#         """
#         asc = " -.:=+*#%@"
#         scale = 10 / (max(array) - min(array))
#         offset = -min(array)
#         self.pix_map = [[0 for j in range(self._width)] for i in range(self._height)]
#         for row in range(self._height):
#             line = ""
#             for col in range(self._width):
#                 pix = int((array[row * self._width + (self._width - col - 1)] + offset) * scale)
#                 self.pix_map[row][col] = pix
#                 try:
# #                     the_char = MLX_Cam.asc[pix]
#                     the_char = asc[pix]
#                     
#                     #print(f"{the_char}{the_char}", end='')
#                 except IndexError: pass
#                     #print("><", end='')
#             #print('')
#         return
# 
# 
#     def get_image(self):
#         """!
#         @brief   Get one image from a MLX90640 camera.
#         @details Grab one image from the given camera and return it. Both
#                  subframes (the odd checkerboard portions of the image) are
#                  grabbed and combined. This assumes that the camera is in the
#                  ChessPattern (default) mode as it probably should be.
#         @returns A reference to the image object we've just filled with data
#         """
#         for subpage in (0, 1):
#             while not self._camera.has_data:
#                 time.sleep_ms(5)
# #                 print('.', end='')
#             self._camera.read_image(subpage)
#             state = self._camera.read_state()
#             image = self._camera.process_image(subpage, state)
# 
#         return image
#     
#     def target_alg(self, xrange):
#         threshhold = 5
# #         x_sum = array.array('i', self._width*[0])
#         sum_old = 0
#         avg_old = 0
#         for col in range(xrange[0], xrange[1] + 1):
#             sum = 0
#             for row in range(self._height):
#                 val = self.pix_map[row][col+1]
#                 if val > threshhold:
#                     sum = sum + val*val
#             avg = int(sum/32)
#             if avg > avg_old:
#                 avg_old = avg
#                 x_target = col+1
#         max_y = 0
#         sum_y = 0
#         count = 0
#         for row in range(self._height):
#             sum_y += self.pix_map[row][x_target]
#         avg_row = sum_y/self._height
#         sum_y_ind = 0
#         sum_y_val = 0
#         for row in range(self._height):
#             if self.pix_map[row][x_target] > avg_row:
#                 sum_y_ind += row
#                 sum_y_val += self.pix_map[row][x_target]*row
# #         print(f"Count: {count}")
#         y_target = sum_y_val/sum_y_ind
#         x_center = self._width/2
#         y_center = self._height/2
#         
# #         print(f"center: ({x_center},{y_center})")
#         print(f"target: ({x_target},{y_target})")
#         # Error is computed with relation to the center of the image.
#         # A positive error_x --> blaster is aimed too far to the right
#         # A positive error_y --> blaster is aimed too high
#         error_x = x_center - x_target
#         error_y = y_target - y_center
#         return error_x, error_y
gc.collect() 
def dual():
    gc.collect()
    initTime = time.ticks_ms()
    try:
        from pyb import info
    # Oops, it's not an STM32; assume generic machine.I2C for ESP32 and others
    except ImportError:
        # For ESP32 38-pin cheapo board from NodeMCU, KeeYees, etc.
        i2c_bus = I2C(1, scl=Pin(22), sda=Pin(21))
    # OK, we do have an STM32, so just use the default pin assignments for I2C1
    else:
        i2c_bus = I2C(1)
    # Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33
    scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
    gc.collect()
    camera = MLX_Cam(i2c_bus)
    gc.collect()
    
    encoder1.zero()
    encoder2.zero()
    
    KP1 = .15
    KP2 = .15
    
    setPoint1 = -5000
    setPoint2 = 0
    
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)
    pyb.delay(1500)
    gc.collect()
    print("Power On")
    
    control1 = Control(KP1, setPoint1 + 32768)
    control2 = Control(KP1, setPoint2 + 32768)
    psi1 = 101
    elapsed = 0
    startTime = time.ticks_ms()
#     while (psi1 > 100):
    while (elapsed < 2000):
        elapsed = time.ticks_ms() - startTime
        pos1 = encoder1.read()
        pos2 = encoder2.read()
        psi1 = control1.run(pos1)
        motor1.set_duty_cycle(-psi1)
        pyb.delay(5)
        
        psi2 = control2.run(pos2)
        motor2.set_duty_cycle(-psi2)
        pyb.delay(5)
        
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)
    
    xrange = [13, 19]
    gc.collect()
    print(f"Elapsed: {time.ticks_ms() - initTime}")
    while (time.ticks_ms() - initTime < 5000):
        image = camera.get_image()
        camera.ascii_art(image)
        print(image)
        Yaw_error, Pitch_error = camera.target_alg(xrange, image)
        setPoint1 = Yaw_error*61
        setPoint2 = Pitch_error*61
        control1 = Control(KP1, setPoint1 + 32768)
        control2 = Control(KP1, setPoint2 + 32768)
        
        encoder1.zero()
        encoder2.zero()
        elapsed = 0
        startTime = time.ticks_ms()
        
#         while (psi1 > 100):
        while (elapsed < 500):
            elapsed = time.ticks_ms() - startTime
            pos1 = encoder1.read()
            pos2 = encoder2.read()
            psi1 = control1.run(pos1)
            motor1.set_duty_cycle(-psi1)
            pyb.delay(5)
            
            psi2 = control2.run(pos2)
            motor2.set_duty_cycle(-psi2)
            pyb.delay(5)
            
        motor1.set_duty_cycle(0)
        motor2.set_duty_cycle(0)
        print("shoot")
        
if __name__ == "__main__":
    dual()
    