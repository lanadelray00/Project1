#include <Stepper.h>

// 함수 선언부 (function prototypes)
void buzzur();
void led_warn(int pin);
void ultra_sonic1();
void ultra_sonic2();

const int stepsPerRevolution = 64; 
Stepper myStepper(stepsPerRevolution, 12, 10, 11, 9); 

const int TRIG_1 = 8;
const int ECHO_1 = 7;
const int TRIG_2 = 6;
const int ECHO_2 = 5;
int speakerpin = 4;
const int led = A3;

unsigned long t_prev_1 = 0;
const unsigned long t_delay_1 = 100;

unsigned long t_prev_2 = 0;
const unsigned long t_delay_2 = 100;

unsigned long t_prev_3 = 0;
const unsigned long t_delay_3 = 200;

long duration1, distance1;
long duration2, distance2;

int i;
int flag;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_1, OUTPUT);
  pinMode(ECHO_1, INPUT);
  pinMode(TRIG_2, OUTPUT);
  pinMode(ECHO_2, INPUT);
  pinMode(led, OUTPUT);

  myStepper.setSpeed(300);
}

void loop() {
  unsigned long t_now_1 = millis();
  if (t_now_1 - t_prev_1 >= t_delay_1) {
    t_prev_1 = t_now_1;
    
    if (i == 0) {
      flag = 1;
    }
    
    if (flag == 1) {   
      i++;
      myStepper.step(stepsPerRevolution);
      ultra_sonic1();
      ultra_sonic2();
      Serial.print(i);
      led_warn(led);
    }
  }

  unsigned long t_now_2 = millis();
  if (t_now_2 - t_prev_2 >= t_delay_2) {
    t_prev_2 = t_now_2;
    
    if (i == 33) {
      flag = -1;
    }
    
    if (flag == -1) {
      i--;
      myStepper.step(-stepsPerRevolution);
      ultra_sonic1();
      ultra_sonic2();
      Serial.print(i);
      led_warn(led);
    }
  }

  unsigned long t_now_3 = millis();
  if (t_now_3 - t_prev_3 >= t_delay_3) {
    t_prev_3 = t_now_3;
    buzzur();
  }
}

void led_warn(int pin) {
  if (distance2 <= 50 || distance1 <= 50) {
    if (digitalRead(pin) == LOW) { 
      digitalWrite(pin, HIGH);
    } else {
      digitalWrite(pin, LOW);
    } 
  } else {
    digitalWrite(pin, LOW);
  }
}

void buzzur() {
  if (distance2 <= 50 || distance1 <= 50) {
    tone(speakerpin, 500, 100);
  }
}

void ultra_sonic1() {
  digitalWrite(TRIG_1, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_1, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_1, LOW);
  duration1 = pulseIn(ECHO_1, HIGH);
  distance1 = duration1 * 17 / 1000;
  Serial.print("\ndistance1 : ");
  Serial.print(distance1);
  Serial.println(" cm");
}

void ultra_sonic2() {
  digitalWrite(TRIG_2, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_2, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_2, LOW);
  duration2 = pulseIn(ECHO_2, HIGH);
  distance2 = duration2 * 17 / 1000;
  Serial.print("\ndistance2 : ");
  Serial.print(distance2);
  Serial.println(" cm");
}
