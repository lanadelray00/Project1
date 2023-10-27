#include <Stepper.h>
#include <Servo.h>

const int TRIG_1 = 4; //TRIG 핀 설정 (초음파 보내는 핀)
const int ECHO_1 = 3; //ECHO 핀 설정 (초음파 받는 핀)
const int TRIG_2 = 7; //TRIG 핀 설정 (초음파 보내는 핀)
const int ECHO_2 = 6; //ECHO 핀 설정 (초음파 받는 핀)

const int ledPin = 13;
char incomingByte;
char inByte;

const int stepsPerRevolution = 64; 
Stepper myStepper(stepsPerRevolution, 11,9,10,8); 

unsigned long t_prev = 0;
const unsigned long t_delay = 200;

int i;
int flag;
int angle_servo = 90;
float angle_step = 0;
// float one_step_angle = 360 / (2048 / stepsPerRevolution);
float one_step_angle = 5.625;
long duration;
int distance;
int danger_distance = 5;
Servo servo;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_1, OUTPUT);
  pinMode(ECHO_1, INPUT);
  pinMode(TRIG_2, OUTPUT);
  pinMode(ECHO_2, INPUT);
  myStepper.setSpeed(300);
  servo.attach(5);
  servo.write(180);
  
  pinMode(ledPin, OUTPUT);
}

void loop() {
  unsigned long t_now = millis();

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

    angle_step = one_step_angle * i;

    // if (distance_2 < danger_distance) {
    //   angle_servo = one_step_angle * i;
      
    //   if (angle_servo > 180) {
    //     angle_servo = 179;
    //   }
    //   else if (angle_servo < 0) {
    //     angle_servo = 1;
    //   }
    //   servo.write(angle_servo);
    // }
      
    Serial.print("Distance:");
    Serial.print(distance_1);
    Serial.print(":");
    Serial.print(distance_2);
    // Serial.print(":");
    // Serial.print(i);
    Serial.print(":");
    Serial.println(angle_step);
    // Serial.print(":");
    // Serial.print(angle_servo);
    // Serial.println(":");
  }

  if (Serial.available()) {
    inByte = Serial.read(); 
    if (inByte == 't') {
      servo.write(angle_servo);
      delay(1000);
      servo.write(0);
      Serial.println("tttttttttttttttt");
    }
  }

  if (Serial.available()) {
    incomingByte = Serial.read();
    if (incomingByte == 'h') {
        digitalWrite(ledPin, HIGH);
    }
    if (incomingByte == 'l') {
        digitalWrite(ledPin, LOW);
    }
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