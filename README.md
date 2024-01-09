# GotoPiScope

GotoPiScope is an advanced Raspberry Pi-based telescope control system, designed to bring automation and precision to your astronomical observations. This project integrates hardware control and software algorithms to point and track celestial objects with ease.

## Features

- **Telescope Positioning:** Control altitude and azimuth of your telescope with stepper motors for precise positioning.
- **Stellarium Integration:** Sync with Stellarium software for real-time celestial tracking.
- **Remote Control:** Operate your telescope remotely, providing flexibility and convenience in observations.
- **Auto-Follow Mode:** Automatically track celestial objects as they move across the sky.
- **Focus Control:** Manage the focus of your telescope through a dedicated focus controller.

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- Stepper Motors for telescope movement
- Rotary Encoders for precise motor control
- Motor Driver Circuitry compatible with Raspberry Pi
- (Optional) Remote control hardware for remote operation

## Software Dependencies

- Python 3
- `pigpio` library for Raspberry Pi GPIO control
- `tkinter` for the GUI
- `requests` for HTTP requests (for Stellarium integration)
- `threading` for parallel processing

## Installation

1. Ensure all hardware components are properly connected to the Raspberry Pi.
2. Install Python 3 on your Raspberry Pi.
3. Install required Python libraries:

   ```bash
   sudo apt-get update
   sudo apt-get install python3-pigpio python3-tk
   pip3 install requests
   ```

4. Clone the repository to your Raspberry Pi:

   ```bash
   git clone https://github.com/lkaesberg/GotoPiScope.git
   ```

5. Navigate to the cloned directory and run the application:

   ```bash
   cd GotoPiScope
   sudo pigpiod
   python3 telescope_app.py
   ```
## Pin Configuration

For successful operation of the GotoPiScope, it's crucial to correctly configure the GPIO pins of the Raspberry Pi. Below is the detailed pin configuration required for the stepper motors and encoder motors used in the system.

### Stepper Motors
The system utilizes three stepper motors: one for altitude control, one for azimuth control, and one for focus control. Each motor is connected to the Raspberry Pi via three pins: a step pin, a direction pin, and an enable pin. 

1. **Altitude Motor**
   - Step Pin: GPIO 13
   - Direction Pin: GPIO 25
   - Enable Pin: GPIO 8

2. **Azimuth Motor**
   - Step Pin: GPIO 12
   - Direction Pin: GPIO 20
   - Enable Pin: GPIO 16

3. **Focus Motor**
   - Step Pin: GPIO 18
   - Direction Pin: GPIO 23
   - Enable Pin: GPIO 24

### Encoders
Encoders provide feedback for precise positioning. The altitude and azimuth motors are each paired with an encoder, requiring two additional GPIO pins for each encoder (channel A and channel B).

1. **Altitude Encoder**
   - Channel A: GPIO 11
   - Channel B: GPIO 7
   - PID Configuration: P=100, I=0, D=1
   - Steps Per Rotation: 2400 * (100/13)

2. **Azimuth Encoder**
   - Channel A: GPIO 15
   - Channel B: GPIO 14
   - PID Configuration: P=100, I=0, D=1
   - Steps Per Rotation: 2400 * (400/40)

### Important Notes
- The `steps_per_rotation` for each motor should be calibrated based on your specific gear ratios and motor characteristics.
- Ensure that the Raspberry Pi is turned off or rebooted after connecting or disconnecting hardware to avoid damage to the GPIO pins.
- Always double-check connections before powering on the Raspberry Pi to ensure they match the specified configuration.

By following this pin configuration, you can ensure the correct setup for the motors and encoders in the GotoPiScope system. This setup is crucial for accurate control and tracking of celestial objects.

## Usage

- Start the GotoPiScope application.
- If using Stellarium, ensure it's running and configured to connect with your Raspberry Pi.
- Use the GUI to move the telescope, set targets, and focus.
- For remote control, ensure your remote device is properly configured and connected.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

- Thanks to the developers of Stellarium for their fantastic astronomy software.
- Gratitude to the Raspberry Pi community for their invaluable resources and support.
