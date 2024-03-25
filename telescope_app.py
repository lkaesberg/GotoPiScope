import time
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import requests
import threading
import read_sbus_from_GPIO
from remote_controller import remote_control

from stepper_motor import StepperMotor
from encoder_motor import EncoderMotor
from telescope import Telescope
from focus_controller import FocusController


class App(ThemedTk):
    def __init__(self, telescope: Telescope, focus_motor: StepperMotor, remote_pin):
        super().__init__()
        self.telescope = telescope
        self.title("Telescope Control")
        self.geometry("600x500")
        self.attributes('-topmost',True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.target = None

        self.set_theme("equilux")  # Set the theme

        style = ttk.Style(self)
        bg_color = style.lookup("TFrame", "background")  # Get the background color of the theme

        self.configure(background=bg_color)

        self.goto_frame = ttk.Frame(self)
        self.goto_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.altitude_label = ttk.Label(self.goto_frame, text="Altitude:")
        self.altitude_label.grid(row=0, column=0, padx=5, pady=5)

        self.altitude_var = tk.StringVar()
        self.altitude_entry = ttk.Entry(self.goto_frame, textvariable=self.altitude_var)
        self.altitude_entry.grid(row=0, column=1, padx=5, pady=5)

        self.azimuth_label = ttk.Label(self.goto_frame, text="Azimuth:")
        self.azimuth_label.grid(row=1, column=0, padx=5, pady=5)

        self.azimuth_var = tk.StringVar()
        self.azimuth_entry = ttk.Entry(self.goto_frame, textvariable=self.azimuth_var)
        self.azimuth_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.goto_button = ttk.Button(self.goto_frame, text="Go To", command=self.goto)
        self.goto_button.grid(row=2, column=1, padx=5, pady=5)
        
        self.error_label = ttk.Label(self, text="")
        self.error_label.grid(row=6, column=2, columnspan=3, padx=5, pady=5)
        
        self.controller_label = ttk.Label(self, text="")
        self.controller_label.grid(row=7, column=2, columnspan=3, padx=5, pady=5)
        
        self.auto_frame = ttk.Frame(self)
        self.auto_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        
        self.auto_follow = False
        self.auto_follow_button = ttk.Button(self.auto_frame, text="Start Auto Follow", command=self.toggle_auto_follow)
        self.auto_follow_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.autofollow_label = ttk.Label(self.auto_frame, text="Target\nNot set!")
        self.autofollow_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        
        self.target_button = ttk.Button(self.auto_frame, text="Set Target", command=self.set_target)
        self.target_button.grid(row=1, column=0, padx=5, pady=5)

        self.sync_button = ttk.Button(self, text="Sync with Stellarium", command=self.update)
        self.sync_button.grid(row=4, column=2, padx=5, pady=5)

        # Control Buttons
        self.control_frame = ttk.Frame(self)
        self.control_frame.grid(row=0, column=2, columnspan=2, padx=10, pady=10)

        button_size = 3  # Adjust this value to change the size of the buttons

        self.up_button = ttk.Button(self.control_frame, text="↑", width=button_size, command=lambda: self.adjust_position(-1, 0))
        self.up_button.grid(row=0, column=1, padx=5, pady=5)

        self.down_button = ttk.Button(self.control_frame, text="↓", width=button_size, command=lambda: self.adjust_position(1, 0))
        self.down_button.grid(row=2, column=1, padx=5, pady=5)

        self.left_button = ttk.Button(self.control_frame, text="←", width=button_size, command=lambda: self.adjust_position(0, 1))
        self.left_button.grid(row=1, column=0, padx=5, pady=5)

        self.right_button = ttk.Button(self.control_frame, text="→", width=button_size, command=lambda: self.adjust_position(0, -1))
        self.right_button.grid(row=1, column=2, padx=5, pady=5)
        
        self.telescope_loop = threading.Thread(target=self.telescope.run, args=[self.on_telescope_loop])
        self.telescope_loop.start()
        
        self.focus_controller = FocusController(focus_motor)
        
        self.remote = read_sbus_from_GPIO.SbusReader(remote_pin)
        self.remote.begin_listen()
        self.remote_loop = threading.Thread(target=remote_control, args=[self.telescope, self.remote, self.focus_controller])
        self.remote_loop.start()

    def goto(self):
        altitude = float(self.altitude_var.get())
        azimuth = float(self.azimuth_var.get())
        self.telescope.goto_coordinates(altitude, azimuth)
        
    def set_target(self):
        try:
            data = self.get_stellarium_data()
            self.autofollow_label.config(text="Target\nNot set!")
        except:
            self.target = None
            return
        self.target = data["name"]
        self.autofollow_label.config(text=f"Target\nName: {data['localized-name']}\nType: {data['type']}")
        
    def on_telescope_loop(self):
        error = self.telescope.get_current_error()
        position = self.telescope.get_current_coordinate()
        error_text = f"Altitude: {position[0]:.2f}°\nAzimuth: {position[1]:.2f}°\nAltitude Error: {error[0]}\nAzimuth Error: {error[1]}"
        self.error_label.config(text=error_text)
        
        self.controller_label.config(text=f"Controller connected: {self.remote.is_connected()}")
        
        

    def update(self):
        data = self.get_stellarium_data()
        altitude = float(data['altitude'])
        azimuth = float(data['azimuth'])
        self.telescope.set_coordinate_offset(altitude, azimuth)

    def get_stellarium_data(self, object_name=None):
        url = f'http://localhost:8090/api/objects/info'
        params = {
            'format': 'json',
            'name': object_name
        }
        response = requests.get(url, params=params)
        response_json = response.json()
        return response_json

    def adjust_position(self, alt_change, az_change):
        # Assuming telescope has a method to adjust position
        self.telescope.adjust_position(alt_change, az_change)

    def toggle_auto_follow(self):
        self.auto_follow = not self.auto_follow
        if self.auto_follow:
            if not self.target:
                return
            self.auto_follow_button.config(text="Stop Auto Follow")
            self.auto_follow_thread = threading.Thread(target=self.auto_follow_target)
            self.auto_follow_thread.start()
        else:
            self.auto_follow_button.config(text="Start Auto Follow")
            # The thread will exit on its next iteration since self.auto_follow is now False

    def auto_follow_target(self):
        while self.auto_follow and self.target:
            data = self.get_stellarium_data(self.target)
            altitude = float(data['altitude'])
            azimuth = float(data['azimuth'])
            self.telescope.goto_coordinates(altitude, azimuth)
            time.sleep(0.1)  # Adjust this value to control how frequently the telescope updates its position
        else:
            self.auto_follow_button.config(text="Start Auto Follow")
            
    def on_closing(self):
        self.telescope.cleanup()
        self.destroy()

alt_motor = StepperMotor(step_pin=13, dir_pin=25, en_pin=8)
az_motor = StepperMotor(step_pin=12, dir_pin=20, en_pin=16)
focus_motor = StepperMotor(step_pin=18, dir_pin=23, en_pin=24)
focus_motor.disable()
alt_steps_per_rotation = 2400 * (100/13)
az_steps_per_rotation = 2400 * (400/40)
alt_encoder_motor = EncoderMotor(alt_motor, channel_A=11, channel_B=7, P = 100,I=0,D = 1, steps_rotation=alt_steps_per_rotation)
az_encoder_motor = EncoderMotor(az_motor, channel_A=15, channel_B=14, P = 100,I=0,D = 1, steps_rotation=az_steps_per_rotation)
telescope = Telescope(alt_encoder_motor, az_encoder_motor)

# Start the GUI
app = App(telescope, focus_motor, 21)
app.mainloop()
