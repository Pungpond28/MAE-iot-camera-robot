# routes.py
from microdot import Microdot, Response
import asyncio
import time
from html_page import HTML_PAGE
from serial_io import write_command
import camera_ai

app = Microdot()
Response.default_content_type = 'text/html'

# --- WATCHDOG VARIABLE ---
# Stores the time (in seconds) of the last valid motor command
last_motor_time = 0

@app.route('/')
async def index(request):
    return HTML_PAGE

@app.route('/move_once')
async def move_once(request):
    global last_motor_time
    last_motor_time = time.time() # Update activity time

    l = request.args.get('l', '0')
    r = request.args.get('r', '0')
    t = request.args.get('t', '250')
    
    cmd = f"o {l} {r}\n"
    # expect_reply=False makes it instant!
    await asyncio.get_running_loop().run_in_executor(None, write_command, cmd, False)
    
    await asyncio.sleep(float(t)/1000)
    
    # Force stop
    await asyncio.get_running_loop().run_in_executor(None, write_command, "o 0 0\n", False)
    return 'OK'

@app.route('/motor')
async def motor(request):
    global last_motor_time
    last_motor_time = time.time() # Update activity time

    l = request.args.get('l', '0')
    r = request.args.get('r', '0')
    cmd = f"o {l} {r}\n"
    
    # CRITICAL FIX: expect_reply=False prevents "freezing" if ESP32 is slow
    await asyncio.get_running_loop().run_in_executor(None, write_command, cmd, False)
    return 'OK'

# --- Keep existing routes for servo, encoders, led, video, reset ---
# (Paste your existing servo/encoder/led/video/reset routes here)
# ...
@app.route('/led')
async def led(request):
    pin = request.args.get('pin', '2')
    state = request.args.get('state', '0')
    cmd = f"l {pin} {state}\n"
    # LED usually needs a reply to confirm, so we keep default (True) or set False if lazy
    resp = await asyncio.get_running_loop().run_in_executor(None, write_command, cmd)
    return resp
    
@app.route('/servo')
async def servo(request):
    sid = request.args.get('id', '0')
    angle = request.args.get('angle', '0')
    cmd = f"s {sid} {angle}\n"
    resp = await asyncio.get_running_loop().run_in_executor(None, write_command, cmd)
    return resp

@app.route('/encoders')
async def encoders(request):
    resp = await asyncio.get_running_loop().run_in_executor(None, write_command, "e\n")
    try:
        left, right = resp.split()
        return {'left': left, 'right': right}
    except:
        return {'left': 0, 'right': 0}

@app.route('/reset')
async def reset(request):
    await asyncio.get_running_loop().run_in_executor(None, write_command, "r\n")
    return 'OK'

@app.route('/video')
async def video(request):
    return Response(body=camera_ai.generate_frames(), headers={
        'Content-Type': 'multipart/x-mixed-replace; boundary=frame'
    })

@app.route('/toggle_ai')
async def toggle_ai(request):
    state = request.args.get('enabled')
    is_enabled = (state == 'true')
    camera_ai.set_ai_enabled(is_enabled)
    return {'status': 'success', 'ai_enabled': is_enabled}
