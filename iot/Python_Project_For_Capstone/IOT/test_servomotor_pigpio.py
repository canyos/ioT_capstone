import RPi.GPIO as GPIO
import pigpio
import time

servoPin_y1 = 12 
servoPin_y2 = 13 
servoPin_p = 40
servoPin_np = 37
servoPin_ny = 35

servo_y1 = pigpio.pi() 
servo_y2 = pigpio.pi() 
servo_y1.set_mode(servoPin_y1, pigpio.OUTPUT)
servo_y2.set_mode(servoPin_y2, pigpio.OUTPUT)

servo_y1.set_PWM_frequency(servoPin_y1, 50)
servo_y1.set_PWM_range(servoPin_y1, 20000) # 1,000,000 / 50 = 20,000us for 100% duty cycle
servo_y2.set_PWM_frequency(servoPin_y2, 50)
servo_y2.set_PWM_range(servoPin_y2, 20000) # 1,000,000 / 50 = 20,000us for 100% duty cycle

SERVO_MAX_DUTY_y1    = 12.3 
SERVO_MIN_DUTY_y1    = 2.4    
SERVO_MAX_DUTY_y2    = 12.3   
SERVO_MIN_DUTY_y2    = 2.4   
SERVO_MAX_DUTY_p    = 11.9   
SERVO_MIN_DUTY_p    = 2.4    
SERVO_MAX_DUTY_np    = 12   
SERVO_MIN_DUTY_np    = 2.3    
SERVO_MAX_DUTY_ny    = 12   
SERVO_MIN_DUTY_ny    = 2.3    



GPIO.setmode(GPIO.BOARD)        
GPIO.setwarnings(False)	
GPIO.setup(servoPin_p, GPIO.OUT)  
GPIO.setup(servoPin_np, GPIO.OUT)  
GPIO.setup(servoPin_ny, GPIO.OUT)  


servo_p = GPIO.PWM(servoPin_p, 50)  
servo_p.start(0)  
servo_np = GPIO.PWM(servoPin_np, 50)  
servo_np.start(0)  
servo_ny = GPIO.PWM(servoPin_ny, 50)  
servo_ny.start(0)  

def setServoPos_y1(degree) :
  if degree > 180 :
    degree = 180
  if degree < 0 :
    degree = 0
  duty = SERVO_MIN_DUTY_y1+(degree*(SERVO_MAX_DUTY_y1-SERVO_MIN_DUTY_y1)/180.0)
  servo_y1.hardware_PWM(servoPin_y1, 50, 10000*duty)
  

def setServoPos_y2(degree) :
  if degree > 180 :
    degree = 180
  if degree < 0 :
    degree = 0
  duty = SERVO_MIN_DUTY_y2+(degree*(SERVO_MAX_DUTY_y2-SERVO_MIN_DUTY_y2)/180.0)
  servo_y2.hardware_PWM(servoPin_y2, 50, 10000*duty)

def setServoPos_p(degree) :
  if degree > 90 :
    degree = 90
  if degree < 0 :
    degree = 0
  duty = SERVO_MIN_DUTY_p+(degree*(SERVO_MAX_DUTY_p-SERVO_MIN_DUTY_p)/180.0)
  servo_p.ChangeDutyCycle(duty)

def setServoPos_np(degree) :
  if degree > 180 :
    degree = 180
  if degree < 0 :
    degree = 0
  duty = SERVO_MIN_DUTY_np+(degree*(SERVO_MAX_DUTY_np-SERVO_MIN_DUTY_np)/180.0)
  servo_np.ChangeDutyCycle(duty)

def setServoPos_ny(degree) :
  if degree > 180 :
    degree = 180
  if degree < 0 :
    degree = 0
  duty = SERVO_MIN_DUTY_ny+(degree*(SERVO_MAX_DUTY_ny-SERVO_MIN_DUTY_ny)/180.0)
  servo_ny.ChangeDutyCycle(duty)

def getDegree(x,y) :
  x_dfr = x-11
  y_dfr = y-15
  x_1pixel = 1.45833333
  y_1pixel = 1.71875
  dyaw_deg = x_dfr * x_1pixel
  dpitch_deg = y_dfr * y_1pixel
  return dyaw_deg, dpitch_deg


def assignDegree(yaw_deg, pitch_deg) :
  if yaw_deg >360 : 
    yaw_deg = 360
  if yaw_deg < 0 :
    yaw_deg = 0

  if yaw_deg <= 180 : 
    degree_y1 = yaw_deg
    degree_y2 = 0
  if yaw_deg > 180 :
    degree_y1 = 180
    degree_y2 = yaw_deg - 180

  if pitch_deg > 90 : 
    pitch_deg = 90
  if pitch_deg <0 :
    pitch_deg = 0
  degree_p = pitch_deg 
  
  return degree_y1, degree_y2, degree_p
