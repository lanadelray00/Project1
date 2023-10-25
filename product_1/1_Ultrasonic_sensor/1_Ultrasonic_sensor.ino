const int TRIG_1 = 9; //TRIG 핀 설정 (초음파 보내는 핀)
const int ECHO_1 = 8; //ECHO 핀 설정 (초음파 받는 핀)
const int TRIG_2 = 7; //TRIG 핀 설정 (초음파 보내는 핀)
const int ECHO_2 = 6; //ECHO 핀 설정 (초음파 받는 핀)


unsigned long t_prev_1 = 0;
const unsigned long t_delay_1 = 500;

unsigned long t_prev_2 = 0;
const unsigned long t_delay_2 = 500;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_1, OUTPUT);
  pinMode(ECHO_1, INPUT);
  pinMode(TRIG_2, OUTPUT);
  pinMode(ECHO_2, INPUT);
}

void loop() {
  unsigned long t_now_1 = millis();
  if(t_now_1 - t_prev_1 >= t_delay_1) {
    t_prev_1 = t_now_1;

  long duration, distance;
  digitalWrite(TRIG_1, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_1, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_1, LOW);
  duration = pulseIn(ECHO_1, HIGH); // 초음파를 받은 시간 (LOW 에서 HIGH 로 )
  distance = duration * 17 / 1000; // cm 로 환산 (34000 / 10000000 /2 를 간단하게)
  Serial.println(duration);
  Serial.print("\nDIstance1 : ");
  Serial.print(distance);
  Serial.println(" cm");
 }

  unsigned long t_now_2 = millis();
  if(t_now_2 - t_prev_2 >= t_delay_2) {
    t_prev_2 = t_now_2;

  long duration, distance;
  digitalWrite(TRIG_2, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_2, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_2, LOW);
  duration = pulseIn(ECHO_2, HIGH); // 초음파를 받은 시간 (LOW 에서 HIGH 로 )
  distance = duration * 17 / 1000; // cm 로 환산 (34000 / 10000000 /2 를 간단하게)
  Serial.println(duration);
  Serial.print("\nDIstance2 : ");
  Serial.print(distance);
  Serial.println(" cm");
 }

}