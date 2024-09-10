import time
import contourthermalcam as ctc
import pandas as pd
import test_servomotor as ts
import threading
import RPi.GPIO as GPIO
import pixel
from math import *
from picamera2 import Picamera2, Preview
from PIL import Image
import server2
import datetime as dt
import cv2

data_array_mod=0
distance = 0
temperature1 = 0
temperature2 = 0 
flag_high_temp=0
highest_x,highest_y = 0,0
yaw_deg=0
pitch_deg= 55/2
np_deg = 167
ny_deg = 90
flag_fire=0
flag_time_inc = 1
flag_inc = 1
temp_history = []
relay = 40
servoPin_np = 37
index = 0


GPIO.setup(relay,GPIO.OUT)
GPIO.setwarnings(False)	
GPIO.setup(servoPin_np, GPIO.IN) 

def save_camera():
    global index
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1080, 1920)}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    picam2.start()
    index = 0

    while True:
        image_name = str(index) + ".jpg"
        picam2.capture_file(image_name)
        img = cv2.imread(image_name)
        img_ccw_90 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imwrite(image_name, img_ccw_90)
        index += 1
        if index == 6:
            index = 0
        time.sleep(1)   


    
    

def flag_save():
    global flag_fire, yaw_deg
    with open('/home/pc/Desktop/flag_fire.txt', 'w') as f:
        try:
            f.write(str(flag_fire))
        except Exception as ex:
            print(ex)

def handler():
    global pitch_deg, yaw_deg, temperature2
    while True:
        get_data()
        inc_deg()
        check_highest_point()
        print(yaw_deg,pitch_deg,temperature2)
        flag_save()
        flag_print()
        time.sleep(1)
        
def flag_print():
    print(f"flag_time_inc:{flag_time_inc} ,flag_inc:{flag_inc} ,flag_high_temp:{flag_high_temp} ,flag_fire:{flag_fire}")


# 0. 센서 데이터 받아오기 (thread)
def get_data():
    try:
        csv_data = pd.read_csv("/home/pc/Desktop/thermalcam.csv",header=None)
        csv_data2 = pd.read_csv("/home/pc/Desktop/sensor_value.csv",header=None)
        arr_data_csv = csv_data[1:]
        global data_array_mod
        global distance   
        global temperature1
        data_array_mod = ctc.reshap_array(arr_data_csv)
        distance = float(csv_data2[0][1])
        temperature1 = csv_data2[1][1]
        
    except Exception as ex:
        get_data()
    
     
# 1.기초적인 시간흐름에 따른 yaw 각도 증감 (thread)
def inc_deg():
    global yaw_deg, pitch_deg, flag_time_inc, flag_inc,np_deg
    if flag_time_inc == 1:
        if flag_inc == 1:
            yaw_deg += 6
            if yaw_deg >= 360:
                flag_inc = 0
        else : 
            yaw_deg -= 6    
            if yaw_deg <= 0:
                flag_inc = 1

    p_deg=pitch_deg
    ts.setServoPos_y(yaw_deg/2)
    ts.setServoPos_p(p_deg)
    
    
# 2. highest point가 최소 70도 이상인지 판단
def check_highest_point():
    global highest_x,highest_y, flag_high_temp, flag_fire, data_array_mod, temperature2,flag_time_inc
    
    highest_x, highest_y = ctc.get_highest_point(data_array_mod)
    temperature2 = data_array_mod[highest_y][highest_x]

    if temperature2>=50:
        flag_time_inc = 0
        flag_fire=1
        flag_high_temp = 1
    elif temperature2>=70:
        flag_high_temp = 1
        flag_time_inc = 0
        

    if flag_high_temp == 1:
        temp_history.append(temperature2)
        
        if len(temp_history) > 15:
            del(temp_history[0])
        if(temperature2)>=50:
            flag_fire=1

    
# 3. 해당 위치로 중심을 이동 (만약 중간이 아니라면 위의 과정 반복)
def move_center():
    global highest_x
    global highest_y 
    global yaw_deg, pitch_deg, temperature2
    print('move center')
    while not((highest_y == 11) and (highest_x == 16)): 
        if temperature2 < 50:  
             break
        highest_x, highest_y = ctc.get_highest_point(data_array_mod)
        dy,dp = ts.getDegree(highest_x, highest_y) #옮길 위치
        yaw_deg = (yaw_deg+dy)%360
        pitch_deg += dp
        pitch_deg = min(pitch_deg,90)
        print(f'x:{highest_x}, y:{highest_y}, dp:{dp}, dy:{dy}')
        time.sleep(2)
    print("end of move center")


# 4. 화재인지 판단 (아닌경우 각도를 틀어버림 최고온점이 화면 밖으로 가도록)
def judge_fire():
    global highest_x, highest_y, flag_fire, index
    threshold = 2
    threshold_deadline=10
    threshold_sum = 0
    threshold_count=0
    is_red = pixel.check_red(highest_x, highest_y, 100)
    check_len =(3-is_red)*5
    while len(temp_history) <= check_len :
        if flag_fire==1:
            return
        time.sleep(0.5)
    temp_arr = temp_history[:]
    for i in range (min(0,len(temp_arr)-check_len),len(temp_arr)-1):
        if temp_arr[i+1]-temp_arr[i]>=threshold:
            threshold_count+=1
            threshold_sum+=temp_arr[i+1]-temp_arr[i]
    if threshold_sum >=threshold_deadline and temp_arr[len(temp_arr)-1]-temp_arr[len(temp_arr)-check_len]>=20:
        flag_fire = 1

def non_fire() : #화재아닌경우 시퀸스
  global flag_inc, pitch_deg, yaw_deg
  pitch_center = (90-55/2)
  yaw_12pixel_deg = 18

  if flag_inc == 1 :
    if yaw_deg>=360-yaw_12pixel_deg:
        yaw_deg-=yaw_12pixel_deg
        flag_inc=0
    else:
        yaw_deg += yaw_12pixel_deg 
  else :
    if yaw_deg<=0+yaw_12pixel_deg:
        yaw_deg+=yaw_12pixel_deg
        flag_inc=1
    else:
        yaw_deg -= yaw_12pixel_deg 
  pitch_deg = pitch_center

 
# 5. 화재이면 거리 측정후 노즐 각도 조절하여 일정시간 동안 물 분사
def nozzle_deg_distance(p_deg, distance,velocity):
    global np_deg , servoPin_np 
    val_old = 0
    for ipd in range (int(p_deg), 0, -1):
        rad2 = radians(ipd)
        rad1 = radians(p_deg)
        val_new = tan(rad2)-tan(rad1)+4.9*distance/pow((velocity*cos(rad2)), 2)
        if (val_old*val_new < 0) or (val_new ==0):
            np_deg = 167-ipd
            print("degree: ",ipd,". distance: ",distance)
            break
        val_old = val_new
    GPIO.setup(servoPin_np, GPIO.OUT)      
    ts.setServoPos_np(np_deg)
    time.sleep(2)
    GPIO.setup(servoPin_np, GPIO.IN)  
    

def spray(ext_time):#물뿌릴때 돌리는 함수
    global np_deg , ny_deg
    for k in range(2):
        for i in range (-10,10,1) :
            for j in range (-10,10,1) : 
                ts.setServoPos_np(np_deg + i/10)
                ts.setServoPos_ny(ny_deg + j/10)
                time.sleep(ext_time/800)
    

def extinguish(ext_time):
    global relay, distance,pitch_deg
    nozzle_deg_distance(pitch_deg,distance, 5)
    GPIO.output(relay,GPIO.HIGH)
    print("물총켜짐")   
    spray(ext_time)
    #time.sleep(ext_time)
    print('물총 꺼짐')
    GPIO.output(relay,GPIO.LOW)


# 6. 처음으로
if __name__ == '__main__':
    
    t = threading.Thread(target=handler)
    t2= threading.Thread(target = save_camera)
    # t3= threading.Thread(target = server2.server_start)
    
    GPIO.output(relay,GPIO.LOW)
    GPIO.setup(servoPin_np, GPIO.OUT)
    ts.setServoPos_np(np_deg)
    time.sleep(2)
    GPIO.setup(servoPin_np, GPIO.IN) 

    t.start()
    t2.start()
    # t3.start()
 
    while True:
        if flag_high_temp == 1:
            move_center()
          
            if flag_fire == 1:
                print("before")
                extinguish(2)
                print("after")
                while temperature2>=50:
                    move_center()
                    extinguish(2)
                GPIO.setup(servoPin_np, GPIO.OUT)
                np_deg = 167          
                ts.setServoPos_np(np_deg)
                time.sleep(2)
                GPIO.setup(servoPin_np, GPIO.IN) 
                flag_time_inc=1
                flag_high_temp=0
                flag_fire=0
                pitch_deg = 55/2

            elif flag_fire ==0:
                judge_fire()
            else:
                non_fire()
                flag_high_temp = 0
                flag_time_inc = 1

    t.join()
    t2.join()
    t3.join()
  

# python /home/pc/Desktop/Python_Project_For_Capstone/IOT/user_main.py