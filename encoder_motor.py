import pigpio
import rotary_encoder
from time import sleep
from stepper_motor import StepperMotor

class EncoderMotor:
    def __init__(self, motor, channel_A, channel_B, P = 1, max_speed = 2000):
        self.motor = motor  # StepperMotor instance
        self.target_position = 0  # Desired encoder position
        self.current_position = 0  # Current encoder position
        self.motor_speed = 0  # Motor speed in Hz
        self.max_speed = max_speed
        self.P = P

        # Initialize the pigpio library.
        self.pi = pigpio.pi()

        # Create an encoder object and associate it with the provided GPIO pins.
        self.decoder = rotary_encoder.decoder(self.pi, channel_A, channel_B, self.encoder_callback)

    def encoder_callback(self, way):
        self.current_position += way

    def set_target_position(self, position):
        self.target_position = position

    def control_loop(self):
        error = (self.target_position - self.current_position) * self.P
        print(error)
        if error > 0:
            self.motor.set_direction(1)
            self.motor_speed = abs(error)  # Simplified speed control for demonstration
        elif error < 0:
            self.motor.set_direction(0)
            self.motor_speed = abs(error)  # Simplified speed control for demonstration
        else:
            self.motor_speed = 0  # Stop the motor if the target position is reached

        self.motor.set_speed(min((self.motor_speed), self.max_speed))

    def run(self):
        try:
            while True:
                self.control_loop()
                sleep(0.1)  # Sleep for a short duration before checking again
        except KeyboardInterrupt:
            self.motor.cleanup()
            self.pi.stop()  # Stop the pigpio library