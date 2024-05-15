# MP4 Thonny Pyhton script file

This script receives data from a UART interface - updated value of the message sending time. It also randomly generates temperature values and sends it to UART.

## Requirements

- MicroPython
- Raspberry Pi Pico connected to your laptop

## Setup

1. Copy the following code into your main script file (e.g., `main.py`).
2. Run this script, then plug Raspberry Pi Pico out.

## Code

```python
import machine
import time
import random
import sys
import uselect

uart = machine.UART(0, baudrate=115200)
sleep_interval = 20  # Default interval
csv_filename = 'data.csv'

def save_to_csv(data):
    with open(csv_filename, 'a') as f:  # Open the file in append mode
        f.write(data + '\n')  # Write the message and a newline character

def read_from_uart():
    if uart.any():
        return uart.readline().decode().strip()  # Read line from UART and strip newline
    return None

while True:
    data = read_from_uart()
    if data:
        if data.startswith('interval='):
            try:
                sleep_interval = int(data.split('=')[1])
                print(f"Interval updated to {sleep_interval} seconds")
                save_to_csv(data) 
            except ValueError:
                print("Invalid interval received")

    temperature = random.uniform(-20.0, 40.0)
    print(temperature)

    time.sleep(sleep_interval)
