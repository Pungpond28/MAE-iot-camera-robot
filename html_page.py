# html_page.py
HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
<title>Robot Control Center</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
/* Basic Settings */
body { font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; background-color: #f4f4f9; }
h1 { text-align: center; color: #333; margin-bottom: 30px; }
h2 { margin-top: 0; color: #555; border-bottom: 2px solid #ddd; padding-bottom: 10px; font-size: 1.2rem; }

/* --- Layout --- */
.main-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: flex-start;
  gap: 20px;
}

/* --- Camera --- */
.camera-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.cam-feed { 
  border: 4px solid #333; 
  border-radius: 8px;
  background: #000; 
  width: 320px; 
  height: 240px; 
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}
.ai-controls { margin-top: 15px; }
.btn-ai { padding: 10px 20px; margin: 0 5px; cursor: pointer; color: white; border: none; border-radius: 5px; font-weight: bold; }
.btn-on { background-color: #28a745; }
.btn-off { background-color: #dc3545; }
.btn-led-on { background-color: #007bff; }
.btn-led-off { background-color: #6c757d; }

/* --- Controls --- */
.control-panel {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  width: 300px;
}

.slider-container { margin-bottom: 15px; }
.slider { width: 100%; }

.dpad {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 50px 50px 50px;
  gap: 5px;
  margin-top: 20px;
}
.dpad button { 
  width: 100%; height: 100%; 
  cursor: pointer; 
  border: 1px solid #ccc; 
  border-radius: 6px;
  background-color: #e9ecef;
  color: #333;
  font-size: 14px;
  font-weight: 600;
  user-select: none; 
  -webkit-user-select: none;
  touch-action: manipulation;
}
.dpad button:active { background-color: #ccc; transform: translateY(2px); }
.dpad .up { grid-column: 2; grid-row: 1; background-color: #dbeafe; }
.dpad .left { grid-column: 1; grid-row: 2; background-color: #dbeafe; }
.dpad .center { grid-column: 2; grid-row: 2; background-color: #f8d7da; color: #721c24; }
.dpad .right { grid-column: 3; grid-row: 2; background-color: #dbeafe; }
.dpad .down { grid-column: 2; grid-row: 3; background-color: #dbeafe; }

.encoder-box { margin-top: 20px; padding-top: 15px; border-top: 1px solid #eee; }
.enc-btn { padding: 5px 10px; margin-top: 5px; cursor: pointer; }
</style>
</head>

<body>

<h1>Robot Control Center</h1>

<div class="main-container">

    <div class="camera-section">
        <img src="/video" class="cam-feed" />
        <div class="ai-controls">
            <button class="btn-ai btn-on" onclick="toggleAI(true)">AI ON</button>
            <button class="btn-ai btn-off" onclick="toggleAI(false)">AI OFF</button>
        </div>
        <div class="ai-controls" style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 10px;">
            <button class="btn-ai btn-led-on" onclick="toggleLED(2, 1)">LED ON</button>
            <button class="btn-ai btn-led-off" onclick="toggleLED(2, 0)">LED OFF</button>
        </div>
    </div>

    <div class="control-panel">
        <h2>Motors</h2>
        <div class="slider-container">
            <label>Speed Left: <span id="pwmLval">150</span></label>
            <input type="range" id="pwmL" min="0" max="255" value="150" class="slider">
        </div>
        <div class="slider-container">
            <label>Speed Right: <span id="pwmRval">150</span></label>
            <input type="range" id="pwmR" min="0" max="255" value="150" class="slider">
        </div>
        <div class="slider-container">
            <label>Step Time (ms):</label>
            <input type="number" id="stepTime" value="250" style="width: 60px; padding: 5px;">
        </div>

        <div class="dpad">
          <button class="up" 
            onclick="stepMove('f')" 
            onmousedown="startMove('f')" onmouseup="stopMove()" onmouseleave="stopMove()"
            ontouchstart="startMove('f')" ontouchend="stopMove()" ontouchcancel="stopMove()">Forward</button>
          
          <button class="left" 
            onclick="stepMove('l')" 
            onmousedown="startMove('l')" onmouseup="stopMove()" onmouseleave="stopMove()"
            ontouchstart="startMove('l')" ontouchend="stopMove()" ontouchcancel="stopMove()">Left</button>
          
          <button class="center" onclick="forceStop()">Stop</button>
          
          <button class="right" 
            onclick="stepMove('r')" 
            onmousedown="startMove('r')" onmouseup="stopMove()" onmouseleave="stopMove()"
            ontouchstart="startMove('r')" ontouchend="stopMove()" ontouchcancel="stopMove()">Right</button>
          
          <button class="down" 
            onclick="stepMove('b')" 
            onmousedown="startMove('b')" onmouseup="stopMove()" onmouseleave="stopMove()"
            ontouchstart="startMove('b')" ontouchend="stopMove()" ontouchcancel="stopMove()">Backward</button>
        </div>
    </div>

    <div class="control-panel">
        <h2>Servos</h2>
        <div class="slider-container">
            <label>Servo 0: <span id="s0val">90</span></label>
            <input type="range" id="s0" min="0" max="180" value="90" class="slider">
        </div>
        <div class="slider-container">
            <label>Servo 1: <span id="s1val">90</span></label>
            <input type="range" id="s1" min="0" max="180" value="90" class="slider">
        </div>
        <div class="slider-container">
            <label>Servo 2: <span id="s2val">90</span></label>
            <input type="range" id="s2" min="0" max="180" value="90" class="slider">
        </div>

        <div class="encoder-box">
            <h2>Encoders</h2>
            <div style="font-family: monospace; font-size: 1.1em; margin-bottom: 10px;">
                L: <span id="encL">0</span> <br>
                R: <span id="encR">0</span>
            </div>
            <button class="enc-btn" onclick="readEnc()">Read</button>
            <button class="enc-btn" onclick="resetEnc()">Reset</button>
        </div>
    </div>
</div>

<script>
const pwmL = document.getElementById('pwmL');
const pwmR = document.getElementById('pwmR');
const pwmLval = document.getElementById('pwmLval');
const pwmRval = document.getElementById('pwmRval');
const stepTime = document.getElementById('stepTime');

pwmL.oninput = () => pwmLval.innerText = pwmL.value;
pwmR.oninput = () => pwmRval.innerText = pwmR.value;

let isHolding = false;

// --- FIXED CALCULATION LOGIC ---
function calc(dir){
  let vL = parseInt(pwmL.value);
  let vR = parseInt(pwmR.value);
  let l = 0, r = 0;

  // แก้ไข: หุ่นตัวนี้ ค่าลบ = เดินหน้า, ค่าบวก = ถอยหลัง
  
  if (dir === 'f') { 
     // Forward: ส่งค่าลบทั้งคู่
     l = -vL; r = -vR; 
  }
  else if (dir === 'b') { 
     // Backward: ส่งค่าบวกทั้งคู่
     l = vL; r = vR; 
  }
  else if (dir === 'l') { 
     // Turn Left: ซ้ายถอย(บวก) ขวาเดินหน้า(ลบ)
     l = vL; r = -vR; 
  }
  else if (dir === 'r') { 
     // Turn Right: ซ้ายเดินหน้า(ลบ) ขวาถอย(บวก)
     l = -vL; r = vR; 
  }
  
  return {l, r};
}

// 1. Step Move (Click and release quickly)
function stepMove(dir){
  if(isHolding) return;
  let {l,r} = calc(dir);
  fetch(`/move_once?l=${l}&r=${r}&t=${stepTime.value}`);
}

// 2. CONTINUOUS MOVE (New "No-Buffer" Logic)
async function startMove(dir){
  if(isHolding) return; // Already moving
  isHolding = true;
   
  let {l,r} = calc(dir);

  // Keep sending commands ONLY while button is held
  while(isHolding) {
      try {
          // 'await' pauses this loop until the server responds "OK"
          // This guarantees we never send more commands than the robot can handle.
          await fetch(`/motor?l=${l}&r=${r}`);
      } catch (error) {
          console.error("Network error, stopping safety:", error);
          isHolding = false; 
          break;
      }
      
      // Optional: Tiny throttle to be nice to the CPU
      // await new Promise(res => setTimeout(res, 20)); 
  }
}

// 3. STOP MOVE (Interrupts immediately)
function stopMove(){
  if(!isHolding) return;

  // 1. Break the 'while' loop in startMove immediately
  isHolding = false;

  // 2. Send STOP command immediately (don't wait for previous loop to finish)
  fetch('/motor?l=0&r=0');

  // 3. Redundancy: Send again in 50ms just to be sure
  setTimeout(() => fetch('/motor?l=0&r=0'), 50);
}

// Red STOP Button
function forceStop(){
    isHolding = false;
    fetch('/motor?l=0&r=0');
    setTimeout(() => fetch('/motor?l=0&r=0'), 50);
}

// --- Servos & Encoders ---
const s0 = document.getElementById('s0');
const s1 = document.getElementById('s1');
const s2 = document.getElementById('s2');

const s0val = document.getElementById('s0val');
const s1val = document.getElementById('s1val');
const s2val = document.getElementById('s2val');

s0.oninput = () => { s0val.innerText = s0.value; fetch(`/servo?id=0&angle=${s0.value}`); };
s1.oninput = () => { s1val.innerText = s1.value; fetch(`/servo?id=1&angle=${s1.value}`); };
s2.oninput = () => { s2val.innerText = s2.value; fetch(`/servo?id=2&angle=${s2.value}`); };

function readEnc(){
  fetch('/encoders').then(r => r.json()).then(d => {
      document.getElementById('encL').innerText = d.left;
      document.getElementById('encR').innerText = d.right;
  });
}
function resetEnc(){ fetch('/reset'); }
function toggleAI(state) { fetch('/toggle_ai?enabled=' + state); }
function toggleLED(pin, state) { fetch(`/led?pin=${pin}&state=${state}`); }
</script>
</body>
</html>
"""