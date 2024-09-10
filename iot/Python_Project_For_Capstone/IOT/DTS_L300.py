# PIN SETUP
# Black :   24(SCE0)
# Yello :   17
# Red   :   19
# Orange:   21
# Brown :   23
# White :   25
import RPi.GPIO as GPIO
import spidev
import time


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

time.sleep(1)

while True:
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
    
    time.sleep(0.6)                          #delay 0.5s
   

GPIO.cleanup()
