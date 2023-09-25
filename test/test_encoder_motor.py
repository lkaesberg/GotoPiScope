import sys
sys.path.append('..')

from encoder_motor import EncoderMotor
from stepper_motor import StepperMotor
from time import sleep

motor = StepperMotor(step_pin=13, dir_pin=25, en_pin=8)
motor1 = StepperMotor(step_pin=12, dir_pin=20, en_pin=16)
encoder_motor = EncoderMotor(motor, channel_A=11, channel_B=7, P = 20)
encoder_motor1 = EncoderMotor(motor1, channel_A=15, channel_B=14, P = 20)
try:
    while True:
        encoder_motor.control_loop()
        encoder_motor1.control_loop()
        sleep(0.1)  # Sleep for a short duration before checking again
except KeyboardInterrupt:
    encoder_motor.motor.cleanup()
    encoder_motor1.motor.cleanup()
    encoder_motor.pi.stop()  # Stop the pigpio library