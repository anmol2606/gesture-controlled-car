# Gesture Controlled Car

Control a robotic car using hand gestures captured by your webcam.  
This project uses MediaPipe, OpenCV, and Arduino via Bluetooth to detect hand movement and control the car in real time.

------------------------------------------------------------

## Features
- Real-time hand tracking using MediaPipe
- 5-zone gesture control (Forward, Backward, Left, Right, Stop)
- Bluetooth-based communication with Arduino
- Motor control using L298N/L293D motor driver
- Smooth performance with multi-threaded Python
- Center block = STOP for safety

------------------------------------------------------------

## Tech Stack

Python:
- OpenCV
- MediaPipe
- PySerial
- Threading

Arduino:
- C++
- SoftwareSerial (Pins 2 & 3 for Bluetooth)
- Motor Driver: L298N / L293D

Hardware:
- HC-05 / HC-06 Bluetooth module
- Arduino UNO / Nano
- Motor driver
- 2 geared motors + wheels
- Power supply
- Laptop webcam

------------------------------------------------------------

## System Architecture

+---------------------------------+&emsp;&emsp;&emsp;&emsp;Bluetooth&emsp;&emsp;&emsp;&emsp;+-----------------------------+<br>
|&emsp;&emsp;&emsp;Python Application&emsp;&emsp;&ensp;| <---------------------------> |&emsp;&emsp;&emsp;Arduino UNO&emsp;&emsp;&emsp;|<br>
| - OpenCV Camera Feed&emsp;&emsp;&emsp;&nbsp;|&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;| - Receives Commands&emsp;&emsp;|<br>
| - Gesture Detection&emsp;&emsp;&emsp;&emsp;&emsp;|&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&nbsp;| - Motor Control Logic&emsp;&emsp;|<br>
| - Grid Mapping&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&nbsp;|&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;+-------------+--------------+<br>
+-----------------+--------------+&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;|<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&nbsp;|&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;|<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&nbsp;|&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;v<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&nbsp;|&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;+-----------+<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&nbsp;+----------------------------------------------------->|&emsp;Motor&emsp;&nbsp;|<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;|&emsp;Driver&emsp;&ensp;|<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;+------------+<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;|<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;v<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Robot Car<br>

------------------------------------------------------------

## Wiring Diagram

Bluetooth Module (HC-05 / HC-06):<br>
HC-05 TX  -> Arduino D2 (SoftwareSerial RX)<br>
HC-05 RX  -> Arduino D3 (SoftwareSerial TX) [use voltage divider]<br>
HC-05 VCC -> 5V<br>
HC-05 GND -> GND<br>

Motor Driver (L298N / L293D):<br>
IN1 -> D10<br>
IN2 -> D11<br>
IN3 -> D12<br>
IN4 -> D13<br>

Voltage Divider for HC-05 RX (REQUIRED):<br>
Arduino D3 (5V) ---[1kΩ]---+---[2kΩ]--- GND<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;|<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;HC-05 RX

------------------------------------------------------------

## Installation

### 1. Install dependencies:
pip install opencv-python mediapipe pyserial

### 2. Upload Arduino code:
Upload gesture_car.ino to Arduino using Arduino IDE.

### 3. Set correct Bluetooth COM port:
Check Device Manager → Ports (COM & LPT)

Edit this line in the Python file:<br>
bluetooth_port = "COM3"

------------------------------------------------------------

## Gesture Control Guide

Only 5 control zones are used:<br>

&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;+-----------+<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;|&nbsp;FORWARD&nbsp;|<br>
+-----------+------------+-----------+<br>
|&emsp;RIGHT&emsp;&nbsp;|&emsp;&ensp;STOP&emsp;&ensp;|&emsp;&nbsp;LEFT&emsp;&ensp;|<br>
+-----------+------------+-----------+<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;|&emsp;&ensp;BACK&emsp;&nbsp;|<br>
&emsp;&emsp;&emsp;&emsp;&emsp;+------------+<br>

Commands:
- Forward  -> f
- Backward -> b
- Left     -> l
- Right    -> r
- Stop     -> s

Gesture detected using INDEX FINGER TIP.

------------------------------------------------------------

## Running the Program

Run:
python gesture_controlled_car.py

A camera window opens. Move your hand into the control blocks and the car will follow.

Press ESC to stop the program.

------------------------------------------------------------

## Project Files

gesture_controlled_car.py    - Main Python gesture script<br>
gesture_car.ino              - Arduino Bluetooth motor code<br>
README.md                    - Documentation<br>

------------------------------------------------------------

## Troubleshooting

Window not showing:
- Run from CMD/PowerShell/Terminal
- Close apps using webcam
- Test webcam:
  python -c "import cv2; cap=cv2.VideoCapture(0); print(cap.read()[0])"

Car not moving:
- Check TX-RX wiring
- Use voltage divider for HC-05 RX
- Check COM port
- Confirm baud rate 9600

Python sending but Arduino not receiving:
- Remove TX/RX wires while uploading Arduino code
- Reconnect after upload
- Use SoftwareSerial Pins 2 and 3
