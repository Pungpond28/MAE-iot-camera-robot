from microdot import Microdot
import serial
import time

# ---------- SERIAL (ESP32) ----------
ser = serial.Serial('/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0', 115200, timeout=1)
time.sleep(2)   # wait ESP32 reset

# ---------- MICRODOT APP ----------
app = Microdot()

# ---------- LED ON ----------
@app.route('/ledon/')
def ledon(request):
    ser.write(b'on\n')
    return 'LED ON'

# ---------- LED OFF ----------
@app.route('/ledoff/')
def ledoff(request):
    ser.write(b'off\n')
    return 'LED OFF'

# ---------- START SERVER ----------
if __name__ == '__main__':
    print("Starting Microdot server...")
    app.run(host='0.0.0.0', port=5000)
