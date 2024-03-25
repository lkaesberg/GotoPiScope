import pigpio
import rotary_encoder
from time import sleep
from stepper_motor import StepperMotor

def angular_distance(angle1, angle2, steps_rotation):
    # Compute the shortest distance between two angles.
    # The result will be in the range -180 to +180.
    delta = angle2 - angle1
    while delta > steps_rotation/2:
        delta -= steps_rotation
    while delta < -steps_rotation/2:
        delta += steps_rotation
    return int(delta)

class EncoderMotor:
    def __init__(self, motor, channel_A, channel_B, P = 1, I = 0.1, D = 0.1,  max_speed = 2000, steps_rotation = 360):
        self.motor = motor  # StepperMotor instance
        self.target_position = 0  # Desired encoder position
        self.current_position = 0  # Current encoder position
        self.motor_speed = 0  # Motor speed in Hz
        self.max_speed = max_speed
        self.P = P
        self.I = I
        self.D = D
        self.previous_error = 0
        self.integral = 0
        
        self.steps_rotation =steps_rotation

        # Initialize the pigpio library.
        self.pi = pigpio.pi()

        # Create an encoder object and associate it with the provided GPIO pins.
        self.decoder = rotary_encoder.decoder(self.pi, channel_A, channel_B, self.encoder_callback)

    def set_steps_rotation(self, steps_rotation: int):
        self.steps_rotation = steps_rotation
        
    def encoder_callback(self, way):
        self.current_position -= way

    def set_target_position(self, position):
        self.target_position = position
        
    def get_current_error(self):
        return angular_distance(self.current_position, self.target_position, self.steps_rotation)

    def control_loop(self):
        error = self.get_current_error()
        self.integral += error
        derivative = error - self.previous_error
        
        motor_command = (error * self.P) + (self.integral * self.I) + (derivative * self.D)
        motor_command = min(max(-2000, motor_command), 2000)
        print(self.current_position)
        
        if motor_command > 0:
            
            self.motor.set_direction(0)
            self.motor_speed = abs(motor_command)  
        elif motor_command < 0:
            self.motor.set_direction(1)
            self.motor_speed = abs(motor_command)
        else:
            self.motor_speed = 0  # Stop the motor if the target position is reached
        
        self.motor.set_speed(min(self.motor_speed, self.max_speed))
        
        self.previous_error = error  # Update the previous error

    def run(self):
        try:
            while True:
                self.control_loop()
                sleep(0.1)  # Sleep for a short duration before checking again
        except KeyboardInterrupt:
            self.motor.cleanup()
            self.pi.stop()  # Stop the pigpio library