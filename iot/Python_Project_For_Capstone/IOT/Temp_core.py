from gpiozero import CPUTemperature
from os import popen
from time import sleep



Temp = CPUTemperature()
while 1:
    print(Temp.temperature)
    f = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
    print("%u MHz" % (int(f.read()) / 1000))
    f = open("/sys/devices/system/cpu/cpu1/cpufreq/scaling_cur_freq")
    print("%u MHz" % (int(f.read()) / 1000))
    f = open("/sys/devices/system/cpu/cpu2/cpufreq/scaling_cur_freq")
    print("%u MHz" % (int(f.read()) / 1000))
    f = open("/sys/devices/system/cpu/cpu3/cpufreq/scaling_cur_freq")
    print("%u MHz" % (int(f.read()) / 1000))
    
    sleep(0.1)
    

