##################################
# MLX90640 Test with Raspberry Pi
##################################
# Real Time Array
# Pin Setup
# VIN   :   1
# GND   :   6
# SCL   :   5
# SDA   :   3
import time,board,busio
import numpy as np
import adafruit_mlx90640

import matplotlib.pyplot as plt

i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ # set refresh rate


mlx_shape = (24,32)

x = np.arange(0, 32, 1)
y = np.arange(0, 24, 1)
XX, YY = np.meshgrid(x, y)


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
    
    
    data_array = (np.reshape(frame,mlx_shape)) # reshape to 24x32
    data_array_mod1 = np.fliplr(data_array)
    data_array_mod2 = np.flipud(data_array_mod1)
   
    

    plt.title("Contour plots")
    plt.contourf(XX, YY, data_array_mod2, alpha=.75, cmap='jet')
    plt.contour(XX, YY, data_array_mod2, colors='black')
    plt.show()
    
    cs = plt.contour(XX, YY, data_array_mod2, colors='black')

    for item in cs.collections:
        for i in item.get_paths():
            v = i.vertices
            X = v[:, 0]
            Y = v[:, 1]
            print(X,Y)