from encoder_motor import EncoderMotor
from time import sleep

class Telescope:
    def __init__(self, alt_motor: EncoderMotor, az_motor: EncoderMotor):
        self.alt_motor = alt_motor
        
        self.az_motor = az_motor
        
        self.alt_offset_steps_stellarium = 0
        self.az_offset_steps_stellarium = 0
        self.running = True
        
    def goto_coordinates(self, alt, az):
        self.alt_motor.set_target_position(int(alt * self.alt_motor.steps_rotation/360) - self.alt_offset_steps_stellarium)
        self.az_motor.set_target_position(int(az * self.az_motor.steps_rotation/360) - self.az_offset_steps_stellarium)
        
    def goto_position(self, alt, az):
        self.alt_motor.set_target_position(alt - self.alt_offset_steps_stellarium)
        self.az_motor.set_target_position(az - self.az_offset_steps_stellarium)
    
    def adjust_position(self, alt_steps, az_steps):
        self.alt_motor.current_position += alt_steps
        self.az_motor.current_position += az_steps
        
    def get_current_positon(self):
        return self.alt_motor.current_position + self.alt_offset_steps_stellarium, self.az_motor.current_position + self.az_offset_steps_stellarium
        
    def get_target_position(self):
        return self.alt_motor.target_position + self.alt_offset_steps_stellarium, self.az_motor.target_position + self.az_offset_steps_stellarium
    
    def get_current_coordinate(self):
        position = self.get_current_positon()
        return position[0] / (self.alt_motor.steps_rotation/360), position[1] / (self.az_motor.steps_rotation/360)
        
    def get_target_coordinate(self):
        position = self.get_target_position()
        return position[0] / (self.alt_motor.steps_rotation/360), position[1] / (self.az_motor.steps_rotation/360)
    
    def get_current_error(self):
        return self.alt_motor.get_current_error(), self.az_motor.get_current_error()
        
    def set_coordinate_offset(self, alt_offset, az_offset):
        self.alt_motor.current_position = 0
        self.alt_motor.target_position = 0
        self.az_motor.current_position = 0
        self.az_motor.target_position = 0
        self.alt_offset_steps_stellarium = int(alt_offset * self.alt_motor.steps_rotation/360)
        self.az_offset_steps_stellarium = int(az_offset * self.az_motor.steps_rotation/360)
                
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
