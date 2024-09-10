import RPi.GPIO as GPIO
import spidev
import time

LED = 21
SCE = 22
spi_chn0 = 0

SPEED_1MHz = 1000000
SPI_MODE3 = 3
OBJECT = 0xA0
SENSOR = 0xA1

iSensor = 0
iObject = 0

def SPI_COMMAND(ADR):
    Data_Buf = [ADR, 0x22, 0x22]
    GPIO.output(SCE, GPIO.LOW)
    time.sleep(0.00001)
    spi.xfer(Data_Buf[0:1])
    time.sleep(0.00001)
    spi.xfer(Data_Buf[1:2])
    time.sleep(0.00001)
    spi.xfer(Data_Buf[2:3])
    time.sleep(0.00001)
    GPIO.output(SCE, GPIO.HIGH)
    return (Data_Buf[2]*256+Data_Buf[1])


GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(SCE, GPIO.OUT)
GPIO.output(SCE, GPIO.HIGH)

spi = spidev.SpiDev()
spi.open(spi_chn0, 0)
spi.mode = 3
spi.max_speed_hz = SPEED_1MHz

time.sleep(0.5)

while True:
    iSensor = spi.xfer2([SENSOR])[0]         #read sensor temperature
    GPIO.output(LED, GPIO.HIGH)              #not necessary
    time.sleep(0.00001)                      #delay 10us = 0.00001s
    iObject = spi.xfer2([OBJECT])[0]         #read object temperature
    GPIO.output(LED, GPIO.LOW)               #not necessary
    time.sleep(0.5)                          #delay 0.5s
    print("Sensor : {:.2f}, Object : {:.2f}".format(iSensor/100, iObject/100))

GPIO.cleanup()
