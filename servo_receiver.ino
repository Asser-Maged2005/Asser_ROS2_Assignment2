#if defined(ESP32)
  #include <ESP32Servo.h>
  #define JOINT1_PIN 13
  #define JOINT2_PIN 26
  #define JOINT3_PIN 14
  #define JOINT4_PIN 27
  #ifndef LED_BUILTIN
    #define LED_BUILTIN 2
  #endif
#else
  #include <Servo.h>
  #define JOINT1_PIN 3
  #define JOINT2_PIN 5
  #define JOINT3_PIN 6
  #define JOINT4_PIN 9
#endif

const int SERVO_PINS[4] = {JOINT1_PIN, JOINT2_PIN, JOINT3_PIN, JOINT4_PIN};
Servo servos[4];
int currentAngles[4] = {90, 90, 90, 90};
bool ledState = false;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  Serial.begin(115200);
  Serial.setTimeout(10);

#if defined(ESP32)
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
#endif

  for (int i = 0; i < 4; i++) {
#if defined(ESP32)
    servos[i].setPeriodHertz(50);
    servos[i].attach(SERVO_PINS[i], 700, 2300);
#else
    servos[i].attach(SERVO_PINS[i], 700, 2300);
#endif
    servos[i].write(currentAngles[i]);
  }

  delay(200);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String line = Serial.readStringUntil('\n');
    line.trim();
    if (line.length() == 0) return;

    int parsed[4];
    int idx = 0;
    int start = 0;

    for (int i = 0; i <= (int)line.length() && idx < 4; i++) {
      if (i == (int)line.length() || line.charAt(i) == ',') {
        parsed[idx++] = constrain(line.substring(start, i).toInt(), 0, 180);
        start = i + 1;
      }
    }

    if (idx == 4) {
      ledState = !ledState;
      digitalWrite(LED_BUILTIN, ledState);
      for (int i = 0; i < 4; i++) {
        currentAngles[i] = parsed[i];
        servos[i].write(currentAngles[i]);
      }
    }
  }
}