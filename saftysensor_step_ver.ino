#include <Stepper.h>

const int TRIG_1 = 4; //TRIG 핀 설정 (초음파 보내는 핀)
const int ECHO_1 = 3; //ECHO 핀 설정 (초음파 받는 핀)
const int TRIG_2 = 7; //TRIG 핀 설정 (초음파 보내는 핀)
const int ECHO_2 = 6; //ECHO 핀 설정 (초음파 받는 핀)

// const int ledPin = 13;
// int incomingByte;

const int stepsPerRevolution = 64; 
Stepper myStepper(stepsPerRevolution, 11,9,10,8); 

unsigned long t_prev = 0;
const unsigned long t_delay = 500;

int i;
int flag;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_1, OUTPUT);
  pinMode(ECHO_1, INPUT);
  pinMode(TRIG_2, OUTPUT);
  pinMode(ECHO_2, INPUT);
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

    unsigned long duration_1, distance_1, duration_2, distance_2;
    digitalWrite(TRIG_1, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_1, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_1, LOW);

    duration_1 = pulseIn(ECHO_1, HIGH);
    distance_1 = duration_1 * 17 / 1000;

    digitalWrite(TRIG_2, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_2, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_2, LOW);

    duration_2 = pulseIn(ECHO_2, HIGH);
    distance_2 = duration_2 * 17 / 1000;

    Serial.print(distance_1);
    Serial.print(",");
    Serial.println(distance_2);
    // Serial.println("cm");
    // Serial.print(i);
  }
}