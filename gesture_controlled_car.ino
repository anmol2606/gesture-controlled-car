#include <SoftwareSerial.h>

// Motor pins
const uint8_t M1_IN1 = 10;
const uint8_t M1_IN2 = 11;
const uint8_t M2_IN1 = 12;
const uint8_t M2_IN2 = 13;

// SoftwareSerial for HC-05/HC-06
// SoftwareSerial(rxPin, txPin)
SoftwareSerial BT(2, 3); // Arduino pin2 = RX (connect to BT TX), pin3 = TX (connect to BT RX)

char dataChar = '\0';

void setup() {
  // Hardware serial for debugging
  Serial.begin(9600);

  // Bluetooth serial (must match module's baud rate)
  BT.begin(9600);
  delay(100);

  // Motor pins as outputs
  pinMode(M1_IN1, OUTPUT);
  pinMode(M1_IN2, OUTPUT);
  pinMode(M2_IN1, OUTPUT);
  pinMode(M2_IN2, OUTPUT);

  // Start stopped
  stopRobot();

  Serial.println("Arduino ready. Waiting for BT commands on pins 2(RX)/3(TX)...");
}

void moveRobot(char motion) {
  switch (motion) {

    case 'f': // forward
      digitalWrite(M1_IN1, LOW);
      digitalWrite(M1_IN2, HIGH);
      digitalWrite(M2_IN1, HIGH);
      digitalWrite(M2_IN2, LOW);
      Serial.println("Forward");
      break;

    case 'b': // backward
      digitalWrite(M1_IN1, HIGH);
      digitalWrite(M1_IN2, LOW);
      digitalWrite(M2_IN1, LOW);
      digitalWrite(M2_IN2, HIGH);
      Serial.println("Backward");
      break;

    case 'r': // right
      digitalWrite(M1_IN1, HIGH);
      digitalWrite(M1_IN2, LOW);
      digitalWrite(M2_IN1, HIGH);
      digitalWrite(M2_IN2, LOW);
      Serial.println("Right");
      break;

    case 'l': // left
      digitalWrite(M1_IN1, LOW);
      digitalWrite(M1_IN2, HIGH);
      digitalWrite(M2_IN1, LOW);
      digitalWrite(M2_IN2, HIGH);
      Serial.println("Left");
      break;

    case 's': // stop
    default:
      stopRobot();
      Serial.println("Stop/Unknown");
      break;
  }
}

void stopRobot() {
  digitalWrite(M1_IN1, LOW);
  digitalWrite(M1_IN2, LOW);
  digitalWrite(M2_IN1, LOW);
  digitalWrite(M2_IN2, LOW);
}

void loop() {

  // Prefer reading from Bluetooth serial
  if (BT.available()) {
    dataChar = (char)BT.read();

    // Ignore CR/LF
    if (dataChar != '\r' && dataChar != '\n') {
      Serial.print("BT recv: ");
      Serial.println(dataChar);
      moveRobot(dataChar);
    }
    delay(50); // small delay for stability
  }

  // Optional: allow commands from USB Serial Monitor
  if (Serial.available()) {
    char c = (char)Serial.read();
    if (c != '\r' && c != '\n') {
      Serial.print("USB recv: ");
      Serial.println(c);
      moveRobot(c);
      delay(50);
    }
  }
}
