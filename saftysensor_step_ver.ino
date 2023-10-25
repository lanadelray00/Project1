#include <Stepper.h>

const int TRIG = 7;
const int ECHO = 6;

// const int ledPin = 13;
// int incomingByte;

const int stepsPerRevolution = 64; 
Stepper myStepper(stepsPerRevolution, 11,9,10,8); 

unsigned long t_prev = 0;
const unsigned long t_delay = 100;

unsigned long t1_prev = 0;
const unsigned long t1_delay = 100;

int i;
int flag;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  myStepper.setSpeed(300);
  
  // pinMode(ledPin, OUTPUT);
}

void loop() {
  unsigned long t_now = millis();

  // if (Serial.available() > 0) {
  //       incomingByte = Serial.read();
  //       if (incomingByte == 'H') {
  //           digitalWrite(ledPin, HIGH);
  //       }
  //       if (incomingByte == 'L') {
  //           digitalWrite(ledPin, LOW);
  //       }
  //   }

  if(t_now - t_prev >= t_delay) {
    t_prev = t_now;
  
    if (i == 0) {
      flag = 1;
    }
    
    if(flag == 1) {   
        i++;
    // 시계 반대 방향으로 한바퀴 회전
    myStepper.step(stepsPerRevolution);
    }

    if(i == 33) {
      flag = -1;
    }

    if (flag == -1) {
      i--;
    // 시계 반대 방향으로 한바퀴 회전
    myStepper.step(-stepsPerRevolution);
    }

    unsigned long duration, distance;
    digitalWrite(TRIG, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);
    duration = pulseIn(ECHO, HIGH);
    distance = duration * 17 / 1000;
    Serial.print("\nDistance:");
    Serial.println(distance);
    // Serial.println("cm");
    // Serial.print(i);
  }
}