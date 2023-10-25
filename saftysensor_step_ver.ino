#include <Stepper.h>

const int TRIG_1 = 5; //TRIG 핀 설정 (초음파 보내는 핀)
const int ECHO_1 = 4; //ECHO 핀 설정 (초음파 받는 핀)
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
long duration;
int distance;

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

    if(i == 16) {
      flag = -1;
    }

    if (flag == -1) {
      i--;
      // 시계 반대 방향으로 한바퀴 회전
      myStepper.step(-stepsPerRevolution);
    }

    unsigned long distance_1, distance_2;
    Sensor(TRIG_1, ECHO_1);
    distance_1 = distance;

    Sensor(TRIG_2, ECHO_2);
    distance_2 = distance;

    Serial.print(distance_1);
    Serial.print(",");
    Serial.println(distance_2);
    // Serial.println("cm");
    Serial.print(i);
  }
}

void Sensor(int TRIG, int ECHO){
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  duration = pulseIn(ECHO, HIGH);
  distance = duration * 17 / 1000;
}