class StepperMotor:
    def __init__(self, step_pin, dir_pin, en_pin):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.en_pin = en_pin
