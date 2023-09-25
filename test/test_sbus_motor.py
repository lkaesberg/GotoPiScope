import RPi.GPIO as GPIO
from time import sleep
import read_sbus_from_GPIO

# Define the SBUS reader
SBUS_PIN = 21  # Pin where SBUS wire is plugged in, BCM numbering
reader = read_sbus_from_GPIO.SbusReader(SBUS_PIN)
reader.begin_listen()

# Define the motor control pins for Motor 1
DIR1 = 25
STEP1 = 13
EN1 = 8

# Define the motor control pins for Motor 2
DIR2 = 20
STEP2 = 12
EN2 = 16

CW = 1
CCW = 0

# Setup pin layout on PI
GPIO.setmode(GPIO.BCM)

# Establish Pins in software for Motor 1
GPIO.setup(DIR1, GPIO.OUT)
GPIO.setup(STEP1, GPIO.OUT)
GPIO.setup(EN1, GPIO.OUT)

# Establish Pins in software for Motor 2
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(STEP2, GPIO.OUT)
GPIO.setup(EN2, GPIO.OUT)

# Initialize the motors
GPIO.output(EN1, 0)
GPIO.output(EN2, 0)
sleep(1)
pi_pwm1 = GPIO.PWM(STEP1, 1)  # initial speed for Motor 1
pi_pwm1.start(5)
pi_pwm2 = GPIO.PWM(STEP2, 1)  # initial speed for Motor 2
pi_pwm2.start(5)

try:
    while True:
        controller_output = reader.translate_latest_packet()
        if controller_output and reader.is_connected():
            # Assume values 1 and 2 from controller_output are for Motor 1 speed and direction respectively
            # And values 3 and 4 are for Motor 2 speed and direction respectively
            speed_value1 = controller_output[1]
            speed_value2 = controller_output[3]
            
            motor_direction1 = CW if speed_value1 < 1000 else CCW
            motor_direction2 = CW if speed_value2 < 1000 else CCW
            
            GPIO.output(DIR1, motor_direction1)
            GPIO.output(DIR2, motor_direction2)
            
            speed1 = 1
            speed2 = 1
            
            if abs(speed_value1 - 1000) > 100:
                speed1 = abs(speed_value1 - 1000) * 3
                
            if abs(speed_value2 - 1000) > 100:
                speed2 = abs(speed_value2 - 1000) * 3
            
            print(f'Motor 1 Speed: {speed1}, Motor 2 Speed: {speed2}')
            
            pi_pwm1.ChangeFrequency(speed1)
            pi_pwm2.ChangeFrequency(speed2)
            
        sleep(0.1)  # sleep for a short duration before reading the controller again

except KeyboardInterrupt:
    print("cleanup")
    GPIO.cleanup()
