import cv2 as cv
import mediapipe as mp
import serial
import time
import threading

# Set Bluetooth Port (Change 'COM7' if needed)
bluetooth_port = "COM7"
baud_rate = 9600

# Initialize Bluetooth
try:
    Arduino = serial.Serial(bluetooth_port, baud_rate, timeout=1)
    time.sleep(2)
    print(f"Connected to Bluetooth on {bluetooth_port}")
except serial.SerialException:
    print(f"Error: Could not connect to Bluetooth on {bluetooth_port}")
    exit()

# Initialize Laptop Camera
def init_camera():
    cam = cv.VideoCapture(0)
    cam.set(3, 640)  # Lower resolution for stability
    cam.set(4, 480)
    return cam

cam = init_camera()

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

last_command = ""

# Function to Process Camera Feed
def camera_loop():
    global last_command, cam
    while True:
        ret, frame = cam.read()

        if not ret:
            print("Camera Error: Restarting camera...")
            cam.release()
            cv.destroyAllWindows()
            time.sleep(1)
            cam = init_camera()
            continue

        frame = cv.flip(frame, 1)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        new_command = "s"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1])
                y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0])

                cv.circle(frame, (x, y), 4, (0, 255, 0), -1)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if 150 <= x <= 250:
                    if y < 150:
                        new_command = 'f'
                    elif y > 250:
                        new_command = 'b'
                elif 150 <= y <= 250:
                    if x < 150:
                        new_command = 'r'
                    elif x > 250:
                        new_command = 'l'

        # Send Bluetooth Command Only If It Changes
        if new_command != last_command:
            Arduino.flushInput()
            Arduino.write(new_command.encode())
            print(f"Sent: {new_command}")
            last_command = new_command
            time.sleep(0.1)

        # Draw Grid
        cv.rectangle(frame, (50, 50), (350, 350), (0, 0, 255), 2)
        cv.line(frame, (150, 50), (150, 350), (0, 0, 255), 1)
        cv.line(frame, (250, 50), (250, 350), (0, 0, 255), 1)
        cv.line(frame, (50, 150), (350, 150), (0, 0, 255), 1)
        cv.line(frame, (50, 250), (350, 250), (0, 0, 255), 1)

        # Show Camera Feed
        cv.imshow('Frame', frame)

        # Exit on 'ESC' key
        key = cv.waitKey(50)
        if key == 27:
            break

# Bluetooth Handling
def bluetooth_loop():
    while True:
        if Arduino.in_waiting:
            data = Arduino.readline().decode('utf-8').strip()
            print(f"Received: {data}")

# Start Threads for Camera & Bluetooth
camera_thread = threading.Thread(target=camera_loop)
bluetooth_thread = threading.Thread(target=bluetooth_loop)

camera_thread.start()
bluetooth_thread.start()

# Wait for threads to finish
camera_thread.join()
bluetooth_thread.join()

# Cleanup
cam.release()
cv.destroyAllWindows()
Arduino.close()
print("Disconnected from Bluetooth")