import RPi.GPIO as GPIO
from time import sleep

class StepperMotor:
    def __init__(self, step_pin, dir_pin, en_pin):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.en_pin = en_pin
        
        # Setup pin layout on PI
        GPIO.setmode(GPIO.BCM)
        
        # Establish Pins in software
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.en_pin, GPIO.OUT)
        
        # Initialize the motor
        GPIO.output(self.en_pin, 0)
        self.pi_pwm = GPIO.PWM(self.step_pin, 1)  # Initial frequency set to 1 Hz for PWM
        self.pi_pwm.start(0)
    
    def set_speed(self, speed):
        """
        Set the speed of the motor by adjusting the frequency of the PWM signal.
        :param speed: Desired speed as a frequency in Hz.
        """
        if speed == 0:
            self.pi_pwm.ChangeDutyCycle(0)  # Stop the motor by setting duty cycle to 0
        else:
            self.pi_pwm.ChangeFrequency(speed)  # Adjust the PWM frequency to control speed
            self.pi_pwm.ChangeDutyCycle(5)

    
    def set_direction(self, direction):
        """
        Set the direction of the motor rotation.
        :param direction: 1 for clockwise, 0 for counterclockwise.
        """
        GPIO.output(self.dir_pin, direction)
    
    def enable(self):
        """
        Enable the motor driver, allowing motor control.
        """
        GPIO.output(self.en_pin, 0)  # Active low enable
    
    def disable(self):
        """
        Disable the motor driver, preventing motor control.
        """
        GPIO.output(self.en_pin, 1)  # Active low enable
    
    def cleanup(self):
        """
        Cleanup the GPIO pins on program termination.
        """
        self.pi_pwm.stop()
        GPIO.cleanup()
        
    def __del__(self):
        """
        Ensure cleanup is called upon deletion of the object.
        """
        self.cleanup()

