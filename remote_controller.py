from telescope import Telescope
from time import sleep
from focus_controller import FocusController

def remote_control(telescope: Telescope, controller, focus_controller: FocusController):
    CW = 1
    CCW = -1
    while telescope.running:
        controller_output = controller.translate_latest_packet()
        if controller_output and controller.is_connected():
            # Assume values 1 and 2 from controller_output are for Motor 1 speed and direction respectively
            # And values 3 and 4 are for Motor 2 speed and direction respectively
            speed_value1 = controller_output[1]
            speed_value2 = controller_output[3]
            focus_speed_value = controller_output[0]
            
            # Catch faulty packets
            if speed_value1 > 2000:
                speed_value1 = 1000
                
            if speed_value2 > 2000:
                speed_value2 = 1000
                
            if focus_speed_value > 2000:
                focus_speed_value = 1000
            
            motor_direction1 = CW if speed_value1 < 1000 else CCW
            motor_direction2 = CW if speed_value2 < 1000 else CCW
            
            speed1 = 0
            speed2 = 0
            update = False
            if abs(speed_value1 - 1000) > 100:
                speed1 = abs(speed_value1 - 1000)
                update = True
                
            if abs(speed_value2 - 1000) > 100:
                speed2 = abs(speed_value2 - 1000)
                update = True
                
            if abs(focus_speed_value - 1000) > 100:
                focus_controller.set_speed((focus_speed_value - 1000)/3)
            else:
                focus_controller.set_speed(0)
            
            if update:
                telescope.adjust_position(int(motor_direction1*speed1/300), int(motor_direction2*speed2/300))
            sleep(0.03)
            