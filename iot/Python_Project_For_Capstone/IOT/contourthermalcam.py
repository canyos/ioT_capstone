import numpy as np
import cv2
import pandas as pd
import time
import matplotlib.pyplot as plt

def get_highest_point(arr):
    x_max = 0
    y_max = 0
    old_val = 0
    for x in range (32):
        for y in range (24):
            
            if (arr[y][x] >= old_val):
                x_max = x
                y_max = y
                old_val = arr[y][x]
    return x_max , y_max

def extract_area(arr,x,y,size):
    if((x-size)<0):
        low_boundary_x = 0
    else:
        low_boundary_x = x - size
    
    if((x+size)>32):     
        high_boundary_x = 32
    else:
        high_boundary_x = x + size

    if((y-size)<0):
        low_boundary_y = 0
    else:
        low_boundary_y = y - size
    
    if((y+size)>24):     
        high_boundary_y = 24
    else:
        high_boundary_y = y + size
 
    exted_area = arr[low_boundary_y:high_boundary_y,low_boundary_x:high_boundary_x]
    return exted_area

def reshap_array(arr):
    mlx_shape1 = (24,32)
    data_array = (np.reshape(arr,mlx_shape1)) # reshape to 24x32
    data_array = data_array.astype(int)
    data_array_1 = np.fliplr(data_array)
    data_array_2 = np.flipud(data_array_1)
    return data_array_2

# while True:
#     try:
#         csv_data = pd.read_csv("/home/pc/Desktop/thermalcam.csv",header=None)
#     except:
#         pass
#         print("Error")

#     start = time.time()
#     arr_data_csv = csv_data[1:]
#     data_array_mod = reshap_array(arr_data_csv)
#     x1,y1 = get_highest_point(data_array_mod)

#     print(get_highest_point(data_array_mod))
#     print(data_array_mod[y1][x1])
#     print(extract_area(data_array_mod, x1, y1, 3))

#     print("time :", time.time() - start)
    
#     time.sleep(0.1)

  
