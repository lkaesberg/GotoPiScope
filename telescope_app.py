import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import requests
import threading

from stepper_motor import StepperMotor
from telescope import Telescope


class App(ThemedTk):
    def __init__(self, telescope):
        super().__init__()
        self.telescope = telescope
        self.title("Telescope Control")
        self.geometry("400x400")

        self.set_theme("equilux")  # Set the theme

        style = ttk.Style(self)
        bg_color = style.lookup("TFrame", "background")  # Get the background color of the theme

        self.configure(background=bg_color)

        self.altitude_label = ttk.Label(self, text="Altitude:")
        self.altitude_label.grid(row=0, column=0, padx=5, pady=5)

        self.altitude_var = tk.StringVar()
        self.altitude_entry = ttk.Entry(self, textvariable=self.altitude_var)
        self.altitude_entry.grid(row=0, column=1, padx=5, pady=5)

        self.azimuth_label = ttk.Label(self, text="Azimuth:")
        self.azimuth_label.grid(row=1, column=0, padx=5, pady=5)

        self.azimuth_var = tk.StringVar()
        self.azimuth_entry = ttk.Entry(self, textvariable=self.azimuth_var)
        self.azimuth_entry.grid(row=1, column=1, padx=5, pady=5)

        self.goto_button = ttk.Button(self, text="Go To", command=self.goto)
        self.goto_button.grid(row=2, column=1, padx=5, pady=5)

        self.sync_button = ttk.Button(self, text="Sync with Stellarium", command=self.update)
        self.sync_button.grid(row=4, column=1, padx=5, pady=5)

        self.up_button = ttk.Button(self, text="Up", command=lambda: self.adjust_position(0, 1))
        self.up_button.grid(row=3, column=1, padx=5, pady=5)

        self.down_button = ttk.Button(self, text="Down", command=lambda: self.adjust_position(0, -1))
        self.down_button.grid(row=5, column=1, padx=5, pady=5)

        self.left_button = ttk.Button(self, text="Left", command=lambda: self.adjust_position(-1, 0))
        self.left_button.grid(row=4, column=0, padx=5, pady=5)

        self.right_button = ttk.Button(self, text="Right", command=lambda: self.adjust_position(1, 0))
        self.right_button.grid(row=4, column=2, padx=5, pady=5)

        self.info_label = ttk.Label(self, text="")
        self.info_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

    def goto(self):
        altitude = float(self.altitude_var.get())
        azimuth = float(self.azimuth_var.get())
        self.telescope.goto(altitude, azimuth)

    def update(self):
        threading.Thread(target=self.fetch_stellarium_data).start()

    def get_stellarium_data(self, object_name=None):
        url = f'http://localhost:8090/api/objects/info'
        params = {
            'format': 'json',
            'name': object_name
        }
        response = requests.get(url, params=params)
        response_json = response.json()
        return response_json

    def fetch_stellarium_data(self):
        data = self.get_stellarium_data()  # Assuming this function fetches data from Stellarium
        info_text = f"Name: {data['localized-name']}\nAltitude: {data['altitude']}\nAzimuth: {data['azimuth']}"
        self.info_label.config(text=info_text)

    def adjust_position(self, az_change, alt_change):
        # Assuming telescope has a method to adjust position
        self.telescope.adjust_position(az_change, alt_change)


alt_motor = StepperMotor(step_pin=18, dir_pin=23, en_pin=24)
az_motor = StepperMotor(step_pin=19, dir_pin=20, en_pin=21)
telescope = Telescope(alt_motor, az_motor)

# Start the GUI
app = App(telescope)
app.mainloop()
