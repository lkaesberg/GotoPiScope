import rotary_encoder
import pigpio
from time import sleep

# Define the GPIO pin numbers for your encoders.
channel_A1 = 11  # Using GPIO17 for encoder 1
channel_B1 = 7  # Using GPIO27 for encoder 1

channel_A2 = 15  # Using GPIO23 for encoder 2
channel_B2 = 14  # Using GPIO24 for encoder 2

position1 = 0  # Current position of encoder 1
position2 = 0  # Current position of encoder 2

old_position1 = 0  # Previous position of encoder 1
old_position2 = 0  # Previous position of encoder 2

def callback1(way):
    global position1
    position1 += way

def callback2(way):
    global position2
    position2 += way

pi = pigpio.pi()  # Initialize the pigpio library.

# Create encoder objects for both encoders and associate them with their respective GPIO pins.
decoder1 = rotary_encoder.decoder(pi, channel_A1, channel_B1, callback1)
decoder2 = rotary_encoder.decoder(pi, channel_A2, channel_B2, callback2)

while True:
    # Print the position of the encoders if a change has occurred.
    if position1 != old_position1 or position2 != old_position2:
        print(f"Encoder 1: pos = {position1} \t Encoder 2: pos = {position2}")
        
        old_position1 = position1
        old_position2 = position2
        
    sleep(0.001)  # Sleep for a short time to reduce CPU load.
