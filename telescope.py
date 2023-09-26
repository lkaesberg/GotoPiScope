from encoder_motor import EncoderMotor
from time import sleep

class Telescope:
    def __init__(self, alt_motor: EncoderMotor, az_motor: EncoderMotor, alt_steps_per_degree, az_steps_per_degree):
        self.alt_motor = alt_motor
        self.alt_steps_per_degree = alt_steps_per_degree
        
        self.az_motor = az_motor
        self.az_steps_per_degree = az_steps_per_degree
        
        self.alt_offset_steps_stellarium = 0
        self.az_offset_steps_stellarium = 0
        self.alt_offset_steps_controller = 0
        self.az_offset_steps_controller = 0
        self.running = True
        
    def goto_coordinates(self, alt, az):
        self.alt_motor.set_target_position(int(alt * self.alt_steps_per_degree) + self.alt_offset_steps_stellarium + self.alt_offset_steps_controller)
        self.az_motor.set_target_position(int(az * self.az_steps_per_degree) + self.az_offset_steps_stellarium + self.az_offset_steps_controller)
        
    def goto_position(self, alt, az):
        self.alt_motor.set_target_position(alt + self.alt_offset_steps_stellarium + self.alt_offset_steps_controller)
        self.az_motor.set_target_position(az + self.az_offset_steps_stellarium + self.az_offset_steps_controller)
    
    def adjust_position(self, alt_steps, az_steps):
        self.alt_offset_steps_controller -= alt_steps
        self.az_offset_steps_controller -= az_steps
        self.goto_position(self.alt_motor.target_position - self.alt_offset_steps_stellarium- self.alt_offset_steps_controller - alt_steps, self.az_motor.target_position - self.az_offset_steps_stellarium - self.az_offset_steps_controller - az_steps)
        
    def get_current_positon(self):
        return self.alt_motor.current_position - self.alt_offset_steps_stellarium - self.alt_offset_steps_controller, self.az_motor.current_position - self.az_offset_steps_stellarium - self.az_offset_steps_controller
        
    def get_target_position(self):
        return self.alt_motor.target_position - self.alt_offset_steps_stellarium - self.alt_offset_steps_controller, self.az_motor.target_position - self.az_offset_steps_stellarium - self.az_offset_steps_controller
    
    def get_current_coordinate(self):
        position = self.get_current_positon()
        return position[0] / self.alt_steps_per_degree, position[1] / self.az_steps_per_degree
        
    def get_target_coordinate(self):
        position = self.get_target_position()
        return position[0] / self.alt_steps_per_degree, position[1] / self.az_steps_per_degree
    
    def get_current_error(self):
        return self.alt_motor.get_current_error(), self.az_motor.get_current_error()
        
    def set_coordinate_offset(self, alt_offset, az_offset):
        self.alt_offset_steps_stellarium = -int(alt_offset * self.alt_steps_per_degree)
        self.az_offset_steps_stellarium = -int(az_offset * self.az_steps_per_degree)
        self.goto_position(-self.alt_offset_steps_stellarium -self.alt_offset_steps_controller, -self.az_offset_steps_stellarium - self.az_offset_steps_controller)
        
    def loop(self):
        self.alt_motor.control_loop()
        self.az_motor.control_loop()
    
    def run(self, callback = None):
        while self.running:
            self.loop()
            if callback:
                callback()
            sleep(0.05)
    
    def cleanup(self):
        self.running = False
        self.alt_motor.motor.cleanup()
        self.az_motor.motor.cleanup()
        self.alt_motor.pi.stop()  # Stop the pigpio library
