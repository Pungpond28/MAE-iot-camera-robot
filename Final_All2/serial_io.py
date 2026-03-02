import serial
import threading
import time

SERIAL_PORT = '/dev/ttyUSB0'
BAUDRATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=0.5)
time.sleep(2)

_lock = threading.Lock()

def write_command(cmd, expect_reply=True):
    with _lock:
        try:
            ser.reset_input_buffer()
            ser.write(cmd.encode())

            if not expect_reply:
                return "OK"

            line = ser.readline().decode().strip()
            return line if line else "NO_REPLY"
        except Exception as e:
            return f"ERR:{e}"


