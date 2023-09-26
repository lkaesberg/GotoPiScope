from stepper_motor import StepperMotor

class FocusController:
    def __init__(self, motor: StepperMotor):
        self.motor = motor
        self.last_speed = 0
        
    def set_speed(self, speed):
        if self.last_speed == 0 and speed != 0:
            self.motor.enable()
        
        if speed == 0 and self.last_speed == 0:
            self.last_speed = speed
            return
        
        if speed == 0:
            self.motor.disable()
        
        self.motor.set_direction(0 if speed > 0 else 1)
        self.motor.set_speed(abs(speed))
        self.last_speed = speed