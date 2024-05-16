import serial


def update_setting(setting, value, ser):
    command = f"{setting}={value}\n"
    try:
        ser.write(command.encode())
        print(f"Updated setting on serial device: {setting} to {value}")
    except serial.serialutil.SerialException as e:
        print(f"Failed to write to serial port: {e}")
