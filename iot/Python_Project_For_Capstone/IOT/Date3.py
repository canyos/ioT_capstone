import RPi.GPIO as GPIO
import spidev
import time
import serial
import numpy as np
import board,busio
import adafruit_mlx90640
import pandas as pd

from multiprocessing import Process

def dts_tfluna() :
    spi_chn0 = 0

    SPEED_1MHz = 100000
    SPI_MODE3 = 3
    OBJECT = 0xA0
    SENSOR = 0xA1

    iSensor = 0
    iObject = 0


    spi = spidev.SpiDev()
    spi.open(spi_chn0, 0)
    spi.mode = 3
    spi.max_speed_hz = SPEED_1MHz

    ser = serial.Serial("/dev/serial0", 115200,timeout=0) 

    def read_tfluna_data():
        while True:
            counter = ser.in_waiting # count the number of bytes of the serial port
            if counter > 8:
                bytes_serial = ser.read(9) # read 9 bytes
                ser.reset_input_buffer() # reset buffer

                if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # check first two bytes
                    distance = bytes_serial[2] + bytes_serial[3]*256 # distance in next two bytes
                    strength = bytes_serial[4] + bytes_serial[5]*256 # signal strength in next two bytes
                    temperature = bytes_serial[6] + bytes_serial[7]*256 # temp in next two bytes
                    temperature = (temperature/8.0) - 256.0 # temp scaling and offset
                    return distance/100.0,strength,temperature


    while True:
        
        if ser.isOpen() == False:
            ser.open() # open serial port if not open

        distance,strength,temperature = read_tfluna_data() # read values
        print('Distance: {0:2.2f} m, Strength: {1:2.0f} / 65535 (16-bit), Chip Temperature: {2:2.1f} C'.\
                    format(distance,strength,temperature)) # print sample data
        ser.close() # close serial port

        isensor = spi.xfer2([SENSOR, 0x22, 0x22]) 
        T_low_byte = isensor[1]
        T_high_byte = isensor[2]
        sensor = T_high_byte<<8 | T_low_byte
        sensor = sensor/100
        
        iobject = spi.xfer2([OBJECT, 0x22, 0x22]) 
        T_low_byte = iobject[1]
        T_high_byte = iobject[2]
        object = T_high_byte<<8 | T_low_byte
        object = object/100
        print("Sensor : {:.2f}, Object : {:.2f}".format(sensor, object))

        # print(spi.xfer2([OBJECT, 0x22, 0x22])) 
    
    
        # iObject = spi.xfer2([OBJECT, 0x22, 0x22])     
        
        time.sleep(1)   
    

    GPIO.cleanup()
    
def thermalcam_func() :
    i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000) # setup I2C
    mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ # set refresh rate
    while True:
        frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
        while True:
            try:
                mlx.getFrame(frame) # read MLX temperatures into frame var
                break
            except ValueError:
                continue # if error, just read again

        # print out the average temperature from the MLX90640
        print('Average MLX90640 Temperature: {0:2.1f}C ({1:2.1f}F)'.\
            format(np.mean(frame),(((9.0/5.0)*np.mean(frame))+32.0)))
        print(frame)
        time.sleep(1)          


if __name__ == '__main__':
    print("main\n")
    p0 = Process(target = dts_tfluna)
    p1 = Process(target = thermalcam_func)
    p0.start()
    p1.start()
    p0.join()
    p1.join()
    