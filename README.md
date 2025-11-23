# 🤖 Gesture Controlled Car

Control a robotic car using hand gestures captured by your webcam!  
This project combines MediaPipe, OpenCV, and Arduino via Bluetooth to recognize directional gestures and move the car in real-time.

## 🔧 Features
- Hand tracking using MediaPipe
- 3×3 grid–based gesture direction detection
- Real-time Bluetooth communication
- Smooth operation using multi-threaded Python
- Control directions: forward, backward, left, right, stop

## 🧰 Tech Stack
Python:
- OpenCV
- MediaPipe
- PySerial
- Threading

Arduino:
- C++ (SoftwareSerial on Pins 2 & 3)
- Motor Driver (L298N / L293D)

Hardware:
- HC-05 / HC-06 Bluetooth module
- Robot chassis
- Motor driver module
- Geared motors
- Battery pack

## 🖥 System Architecture
+------------------+         Bluetooth         +------------------------+
|  Python Program  |  <--------------------->  |      Arduino UNO       |
| - Camera (OpenCV)|                           | - Receives commands    |
| - Gesture Detect |                           | - Motor control logic  |
| - Grid Mapping   |                           +-----------+------------+
+--------+---------+                                       |
         |                                                  |
         |                                                  v
         |                                            +-----------+
         +------------------------------------------->| Motor     |
                                                      | Driver    |
                                                      +-----------+
                                                           |
                                                           v
                                                    Robot Car

## 🧩 Wiring (Bluetooth on Pins 2 & 3)

HC-05 TX  → Arduino D2 (SoftwareSerial RX)  
HC-05 RX  → Arduino D3 (SoftwareSerial TX) [Use voltage divider]  
HC-05 VCC → 5V  
HC-05 GND → GND  

Motor Driver:  
IN1 → D10  
IN2 → D11  
IN3 → D12  
IN4 → D13  

### Voltage Divider for HC-05 RX (required!)
Arduino D3 (5V) ---[1kΩ]---+---[2kΩ]--- GND  
                           |  
                       HC-05 RX

## 📦 Installation

### 1. Install Python Dependencies
pip install opencv-python mediapipe pyserial

### 2. Upload Arduino Code
Upload your .ino file using Arduino IDE.

### 3. Set Bluetooth COM Port
Check Device Manager → Ports (COM & LPT)  
Replace "COM9" inside Python script.

## 🖐 Gesture Detection (3×3 Grid)

+-----------+-----------+-----------+
|           |     F     |           |
|           | (Forward) |           |
+-----------+-----------+-----------+
|     R     |     S     |     L     |
|  (Right)  |   (Stop)  |   (Left)  |
+-----------+-----------+-----------+
|           |     B     |           |
|           | (Backward)|           |
+-----------+-----------+-----------+

Index finger tip position determines the command:
- Top center → Forward (f)
- Middle left → Right (r)
- Middle right → Left (l)
- Bottom center → Backward (b)
- Center → Stop (s)

## ▶ Running the Project
python gesture_car.py

A window titled "Frame" will open.  
Move your hand inside the grid and the car will follow your gesture.

## 🔍 Troubleshooting

Window not showing:
- Must run from a real terminal (CMD/PowerShell)
- Run camera loop in the main thread
- Test webcam:
  import cv2
  cv2.imshow("test", cv2.VideoCapture(0).read()[1])
  cv2.waitKey(0)

Car not moving:
- Ensure voltage divider on HC-05 RX
- Use SoftwareSerial pins 2 & 3
- Check TX↔RX wiring
- Match baud rate (9600)

Python sending but Arduino not receiving:
- Remove TX/RX wires while uploading Arduino code
- Reconnect after upload

## 🚀 Future Improvements
- Add custom gesture training
- Speed control based on hand distance
- Add obstacle detection
- Add Android app control
- Use full-hand bounding box instead of fingertip

## ⭐ Support
If you like this project, please star the repository!
