import RPi.GPIO as GPIO
from time import sleep

ledpin = 36			# PWM pin connected to LED
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
pi_pwm = GPIO.PWM(ledpin,50)		#create PWM instance with frequency
pi_pwm.start(0)				#start PWM of required Duty Cycle 




while True:
    for duty in range(0,130,1):
        pi_pwm.ChangeDutyCycle(duty/10) #provide duty cycle in the range 0-100
        sleep(0.01)
        print(duty)
    
    
    for duty in range(130,-1,-1):
        pi_pwm.ChangeDutyCycle(duty/10)
        sleep(0.01)
        print(duty)
    sleep(0.5)
    pi_pwm.ChangeDutyCycle(65/10)
        