# 🤖 Gesture Controlled Car

Control a robotic car using **hand gestures** captured by your webcam!  
This project combines **MediaPipe**, **OpenCV**, and **Arduino via Bluetooth** to recognize directional gestures and move the car forward, backward, left, and right.

## 🔧 Features
- Hand tracking using MediaPipe
- Grid-based gesture detection
- Real-time communication with Arduino via Bluetooth
- Multi-threaded Python script for smooth camera and Bluetooth handling

## 🧰 Tech Stack
- Python
  - OpenCV
  - MediaPipe
  - pySerial
- Arduino (C++)
- Hardware: Bluetooth module, motor driver, wheels, battery

## 📂 Project Structure
- `gesture_controlled_car.py` - Python script for gesture recognition and Bluetooth commands
- `gesture_controlled_car.ino` - Arduino sketch for receiving Bluetooth commands and controlling the car

## 🖥️ How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/gesture-controlled-car.git
   cd gesture-controlled-car
