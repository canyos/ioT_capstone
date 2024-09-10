import RPi.GPIO as GPIO
from time import sleep
# y1_min = 2.4
# y1_max = 12.3
# 2.4 ~ 12.3반시계방향으로 각도 증가 
# y2_min = 2.4
# y2_max = 12.3
# p_min = 2.4
# p_max = 11.9
# small_min = 2.3
# small_max = 12

#ledpin = 36			# PWM pin connected to LED
relay = 37
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(relay,GPIO.OUT)
# GPIO.setup(relay,GPIO.OUT)
pi_pwm = GPIO.PWM(relay,50)		#create PWM instance with frequency
pi_pwm.start(0)				#start PWM of required Duty Cycle 

#np min 1.5
#np max  11
while True : 
    # GPIO.output(relay,GPIO.HIGH)
    # sleep(1)
    # print('1')
    # GPIO.output(relay,GPIO.LOW)
    # sleep(1)
    duty =1.5
    pi_pwm.ChangeDutyCycle(duty)
    sleep(3)
    print(duty)
    duty = 11
    pi_pwm.ChangeDutyCycle(duty)
    sleep(3)
    print(duty)
    
    # GPIO.output(relay,GPIO.HIGH)
    # sleep(2)
    # GPIO.output(relay,GPIO.LOW)
    # sleep(2)
    


  