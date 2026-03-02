# camera_ai.py
import cv2
import asyncio
from ultralytics import YOLO

# Settings
WIDTH = 320
HEIGHT = 240
detect_every = 3

# Global variables
ai_enabled = True
cap = None
model = None

def init_resources():
    global cap, model
    if cap is None:
        cap = cv2.VideoCapture(0)
    if model is None:
        model = YOLO("yolov8s-world.pt")
        model.set_classes(["helmet", "glasses", "mask"])

def set_ai_enabled(enabled):
    global ai_enabled
    ai_enabled = enabled

async def generate_frames():
    global cap, model, ai_enabled
    
    # Initialize camera/model if not ready
    init_resources()
    
    frame_count = 0
    last_results = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame_count += 1

        if ai_enabled:
            # Run detection periodically
            if frame_count % detect_every == 0:
                # Run blocking YOLO prediction in a separate thread to prevent 
                # blocking the robot motor controls
                loop = asyncio.get_running_loop()
                last_results = await loop.run_in_executor(
                    None, 
                    lambda: model.predict(frame, imgsz=160, conf=0.3, verbose=False)
                )

            # Draw results
            if last_results:
                for result in last_results:
                    for box, conf, cls_id in zip(result.boxes.xyxy, result.boxes.conf, result.boxes.cls):
                        x1, y1, x2, y2 = map(int, box)
                        label = f"{model.names[int(cls_id)]} {conf:.2f}"
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x1, y1 - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        
        # Yield the frame for the browser
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
        # Important: Sleep 0 allows other async tasks (like motors) to run
        await asyncio.sleep(0)
