import threading
import serial
import requests
from app import create_app
from datetime import datetime

flask_app = create_app()


def read_from_serial(port, baudrate, stop_event):
    try:
        serial_connection = serial.Serial(port, baudrate)
        while not stop_event.is_set():
            data = serial_connection.readline().decode().strip()
            if data:
                try:
                    # Prepare data for POST request
                    post_data = {
                        "temp": float(data)
                    }
                    # Send POST request to Flask API endpoint
                    response = requests.post("http://localhost:3000/api/measurements", json=post_data)
                    print(f"POST response: {response.status_code}, {response.content.decode()}")
                except ValueError:
                    print(f"Invalid data received: {data}")
                except requests.exceptions.RequestException as e:
                    print(f"Failed to send POST request: {e}")
    except serial.serialutil.SerialException as e:
        print(f"Error opening serial port: {e}")
    finally:
        serial_connection.close()


# Define the parameters for the serial connection
port = '/dev/tty.usbmodem1101'
baudrate = 115200
stop_event = threading.Event()


def start_serial_reader():
    serial_thread = threading.Thread(target=read_from_serial, args=(port, baudrate, stop_event))
    serial_thread.daemon = True
    serial_thread.start()
    return serial_thread


def stop_serial_reader(serial_thread):
    stop_event.set()
    serial_thread.join()  # Wait for the thread to finish


if __name__ == '__main__':
    serial_thread = start_serial_reader()
    try:
        flask_app.run(host='0.0.0.0', port=3000, debug=True, use_reloader=False)
    finally:
        stop_serial_reader(serial_thread)
