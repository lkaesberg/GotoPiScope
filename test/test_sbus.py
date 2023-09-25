import read_sbus_from_GPIO

SBUS_PIN = 21 #pin where sbus wire is plugged in, BCM numbering

reader = read_sbus_from_GPIO.SbusReader(SBUS_PIN)
reader.begin_listen()

while True:
    print(reader.translate_latest_packet())