import RPi.GPIO as GPIO
from time import sleep

# Direction pin from controller
DIR = 18
# Step pin from controller
STEP = 15
EN = 14
# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

# Setup pin layout on PI
GPIO.setmode(GPIO.BCM)

# Establish Pins in software
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)

# Set the first direction you want it to spin

dir = CW
speed = 200
GPIO.output(EN, 0)
GPIO.output(DIR, dir)
sleep(1)

pi_pwm = GPIO.PWM(STEP, speed)
pi_pwm.start(5)

try:
    # Run forever.
    while True:
        sleep(5.0)
        speed += 200
        print(speed)
        pi_pwm.ChangeFrequency(speed)
        dir = not dir
        GPIO.output(DIR, dir)

# Once finished clean everything up
except KeyboardInterrupt:
    print("cleanup")
    GPIO.cleanup()
