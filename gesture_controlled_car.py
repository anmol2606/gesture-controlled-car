import cv2 as cv
import mediapipe as mp
import serial
import time
import threading

# GLOBAL STOP FLAG
stop_program = False

# Set Bluetooth Port
bluetooth_port = "COM3"
baud_rate = 9600

# Initialize Bluetooth
try:
    Arduino = serial.Serial(bluetooth_port, baud_rate, timeout=1)
    time.sleep(2)
    print(f"Connected to Bluetooth on {bluetooth_port}")
except serial.SerialException:
    print(f"Error: Could not connect to Bluetooth on {bluetooth_port}")
    exit()

# Initialize Camera
def init_camera():
    cam = cv.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    return cam

cam = init_camera()

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

last_command = ""

# CAMERA LOOP
def camera_loop():
    global last_command, cam, stop_program

    while not stop_program:
        ret, frame = cam.read()

        if not ret:
            print("Camera Error: Restarting...")
            cam.release()
            cv.destroyAllWindows()
            time.sleep(1)
            cam = init_camera()
            continue

        frame = cv.flip(frame, 1)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        new_command = "s"  # STOP by default

        # Hand Detection
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1])
                y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0])

                cv.circle(frame, (x, y), 5, (0, 255, 0), -1)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Movement Logic (Only 5 blocks)
                if 150 <= x <= 250:
                    if y < 150:
                        new_command = 'f'  # FORWARD
                    elif y > 250:
                        new_command = 'b'  # BACKWARD

                if 150 <= y <= 250:
                    if x < 150:
                        new_command = 'r'  # RIGHT
                    elif x > 250:
                        new_command = 'l'  # LEFT

        # Send Bluetooth Command ONLY IF CHANGED
        if new_command != last_command:
            Arduino.flushInput()
            Arduino.write(new_command.encode())
            print(f"Sent: {new_command}")
            last_command = new_command
            time.sleep(0.1)

        # 🔵 DRAW ONLY 5 CONTROL BLOCKS (no corner blocks)
        # Vertical Forward-Backline
        cv.rectangle(frame, (150, 50), (250, 150), (0, 0, 255), 2)   # FORWARD
        cv.rectangle(frame, (150, 250), (250, 350), (0, 0, 255), 2) # BACKWARD

        # Horizontal Left-Rightline
        cv.rectangle(frame, (50, 150), (150, 250), (0, 0, 255), 2)  # RIGHT
        cv.rectangle(frame, (250, 150), (350, 250), (0, 0, 255), 2) # LEFT

        # STOP (CENTER BLOCK)
        cv.rectangle(frame, (150, 150), (250, 250), (0, 255, 0), 2)

        # LABELS
        cv.putText(frame, "FORWARD", (150, 90), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv.putText(frame, "BACK", (180, 330), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv.putText(frame, "RIGHT", (60, 200), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv.putText(frame, "LEFT", (270, 200), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv.putText(frame, "STOP", (180, 220), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Show camera feed
        cv.imshow("Frame", frame)

        # ESC to exit
        key = cv.waitKey(1)
        if key == 27:
            stop_program = True
            break

# BLUETOOTH THREAD
def bluetooth_loop():
    global stop_program
    while not stop_program:
        if Arduino.in_waiting:
            data = Arduino.readline().decode(errors="ignore").strip()
            print(f"Received: {data}")

# Start Threads
camera_thread = threading.Thread(target=camera_loop)
bluetooth_thread = threading.Thread(target=bluetooth_loop)

camera_thread.start()
bluetooth_thread.start()

# Main Wait Loop
while not stop_program:
    time.sleep(0.1)

# Cleanup
cam.release()
cv.destroyAllWindows()
Arduino.close()
print("Disconnected from Bluetooth. Program Ended.")
