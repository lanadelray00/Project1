#include <MFRC522.h>
#include <SPI.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <Servo.h>

#define RST_PIN 9
#define SS_PIN 10

Servo servo1;
Servo servo2;

MFRC522 rfid(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;
LiquidCrystal_I2C lcd(0x27, 16, 2);

const int TRIG1 = 4;
const int ECHO1 = 3;
const int TRIG2 = 7;
const int ECHO2 = 6;
const int R_LED = A0;
const int G_LED = A1;
const int B_LED = A2; 
const int buzzerPin = A3;

// card_1 73 BF 0D 12
// card_2 C3 61 8E 12
// card_3 A3 C5 C0 12
// card_4 83 03 B8 12
// card_5 53 ef ae 10

int flag_allow = 1;
byte nuidPICC[4];
String uid;
String string_uid;

String card_1 = "73 bf 0d 12";
String card_2 = "c3 61 8e 12";
String card_3 = "a3 c5 c0 12";
String card_4 = "83 03 b8 12";
String card_5 = "53 ef ae 10";

String admin = "73 bf 0d 12, c3 61 8e 12, 53 ef ae 10";  // 승인된 카드 uid
String not_admin = "a3 c5 c0 12, 83 03 b8 12";  // 승인되지 않은 카드 uid

int min = 10000;
int max = 0;
int angle = 0;
int peopleCount = 0;  // 건물 안에 있는 사람 수

bool standIn = false;
bool standOut = false;

bool checkIn = false;
bool checkOut = false;

unsigned long eventTime = 0; // 이벤트 발생 시간
unsigned long eventIn = 0; // 이벤트 발생 시간
unsigned long eventOut = 0; // 이벤트 발생 시간
unsigned long currentTime;
unsigned long checkTime;
unsigned int flag = 0;

char inByte;
bool mode = true;
bool flag_print = true;

void setup() {
  Serial.begin(9600);
  servo1.attach(5);
  servo2.attach(8);
  pinMode(TRIG1, OUTPUT);
  pinMode(ECHO1, INPUT);
  pinMode(TRIG2, OUTPUT);
  pinMode(ECHO2, INPUT);
  pinMode(buzzerPin, OUTPUT);

  SPI.begin();

  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }

  for (byte i = 0; i < 6; i++) {
    nuidPICC[i] = 0;
  }

  servo1.write(0);
  servo2.write(0);

  lcd.begin();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Please tag");
  lcd.setCursor(0,1);
  lcd.print("your employee ID");
}

String dump_byte_array(byte *buffer, byte bufferSize) {
  String output = "";
    for (byte i = 0; i < bufferSize; i++) {
        //Serial.print(buffer[i] < 0x10 ? " 0" : " ");
        //Serial.print(buffer[i], HEX);
        output += buffer[i] < 0x10 ? " 0" : " ";
        output += String(buffer[i], HEX);
    }
    output = output.substring(1, 12);
    return output;
}

void loop() {
  if (Serial.available()) {
    inByte = Serial.read();

    if (inByte == 'a') {
      servo1.write(90);
    }
    
    else if (inByte == 'b') {
      servo1.write(0);
    }

    if (inByte == 'c') {
      servo2.write(180);
    }

    else if (inByte == 'd') {
      servo2.write(0);
    }

    else if (inByte == 'o') {
      mode = true;
      
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Changed to");
      lcd.setCursor(0,1);
      lcd.print("Auto-control");
      delay(1000);

      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Auto-control");
      lcd.setCursor(0,1);
      lcd.print("mode. Welcome.");
    }

    else if (inByte == 'm') {
      mode = false;

      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Changed to");
      lcd.setCursor(0,1);
      lcd.print("Manual-mode.");
      delay(1000);
    }
  }

  long duration1, distance1;
  long duration2, distance2;

  digitalWrite(TRIG1, LOW);                                                                                                                                                                                                                                                                      
  delayMicroseconds(2);
  digitalWrite(TRIG1, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG1, LOW);
  duration1 = pulseIn(ECHO1, HIGH);

  digitalWrite(TRIG2, LOW);                                                                                                                                                                                                                                                                      
  delayMicroseconds(2);
  digitalWrite(TRIG2, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG2, LOW);
  duration2 = pulseIn(ECHO2, HIGH);

  distance1 = duration1 * 17 / 1000;
  distance2 = duration2 * 17 / 1000;

  Serial.print(distance1);
  Serial.print(", ");
  Serial.println(distance2);

  if (flag_print == true) {
    Serial.print("peopleCount");
    Serial.print(' ');
    Serial.print(peopleCount);
    Serial.print(' ');
    Serial.print(checkIn);
    Serial.print(' ');
    Serial.print(checkOut);
    Serial.print(' ');
    Serial.print(mode);
    Serial.println();
    // Serial.print(flag_allow);
    // Serial.println();
  }

  checkIn = false;
  
  if (mode == true) {
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Please tag");
    lcd.setCursor(0,1);
    lcd.print("your employee ID");
  }

  else if (mode == false) {
    checkOut = false;
    // flag_allow == -1;
    flag_print = true;

    if (distance1 < 7 && distance2 >= 7 && standIn == false && standOut == false && millis() - eventOut >= 5000) {
      // 사람이 건물 안으로 들어온 경우
      servo2.write(90);
      eventIn = millis();
      standIn = true;
      standOut = false;
      flag = 1;
      // delay(1000);
      flag_allow = 1;
      for (byte i = 0; i < 6; i++) {
        nuidPICC[i] = 0;
      }
    }
    
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Manual-mode.");
    lcd.setCursor(0,1);
    lcd.print("Welcome.");
  }

  // Serial.println(flag_allow);

  if (flag_allow == -1) {
    if (distance1 < 7 && distance2 >= 7 && standIn == false && standOut == false && millis() - eventOut >= 5000) {
      // 사람이 건물 안으로 들어온 경우
      if (mode == true) {
      servo1.write(0);
      }
      servo2.write(90);
      eventIn = millis();
      standIn = true;
      standOut = false;
      flag = 1;
      // delay(1000);
      flag_allow = 1;
      for (byte i = 0; i < 6; i++) {
        nuidPICC[i] = 0;
      }
    }
  }

  if (distance1 >= 7 && distance2 < 7 && standIn == true && standOut == false) {
    // 사람이 건물 안으로 들어오는 경우
    servo2.write(90);
    peopleCount++;
    Serial.println("\n 사람이 들어왔습니다.");
    Serial.print("건물 안에 있는 사람 수: ");
    Serial.println(peopleCount);
    standIn = false;
    standOut = false;
    
    checkIn = true; // 건물 안으로 들어 옴!
    checkTime = millis();
    flag = 0;
    // delay(2000);
  }

  if (distance1 >= 7 && distance2 < 7 && standIn == false && standOut == false && millis() - eventIn >= 5000) {
    // 사람이 건물 밖으로 나가는 경우
    eventOut = millis();
    servo2.write(90);
    checkIn = false; 
    standIn = false;
    standOut = true;
    flag = 1;
    // delay(1000);

    // Serial.println("사람이 들어왔습니다.");
  }

  if (distance1 < 7 && distance2 >= 7 && standIn == false && standOut == true) {
    // 사람이 건물 밖으로 나간 경우
    servo2.write(90);
    if (peopleCount >= 1){
      peopleCount--;
    }
    Serial.println("사람이 나갔습니다.");
    Serial.print("건물 안에 있는 사람 수: ");
    Serial.println(peopleCount);
  
    standIn = false;
    standOut = false;

    checkOut = true;
    checkTime = millis();
    flag = 0;
    
    Serial.print("peopleCount");
    Serial.print(' ');
    Serial.print(peopleCount);
    Serial.print(' ');
    Serial.print(checkIn);
    Serial.print(' ');
    Serial.print(checkOut);
    Serial.print(' ');
    Serial.print(mode);
    Serial.println();

    flag_print = false;
    // delay(3000);
  }

  if (distance1 >= 7 && distance2 >= 7 && standIn == false && standOut == false){
    servo2.write(0);
  }

  // StandIn 또는 StandOut 후 10초 지나면 reset
  if (distance1 >= 7 && distance2 >= 7 && standIn == true || standOut == true){
    // Serial.print(millis());
    if (((millis() - eventIn > 5000 && millis() - eventIn < 7000)|| (millis() - eventOut > 5000 && millis() - eventOut < 7000)) && flag == 1){
      standIn = false;
      standOut = false;
    }
  }

    if ( ! rfid.PICC_IsNewCardPresent())
      return;

    if ( ! rfid.PICC_ReadCardSerial())
      return;

  if (mode == false) {
    if (rfid.uid.uidByte[0] != nuidPICC[0] || 
      rfid.uid.uidByte[1] != nuidPICC[1] || 
      rfid.uid.uidByte[2] != nuidPICC[2] || 
      rfid.uid.uidByte[3] != nuidPICC[3] ) {
      
      analogWrite(R_LED, 255);
      analogWrite(G_LED, 0);
      analogWrite(B_LED, 0);
      Serial.println("수동모드 중 인증 시도.");

      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Manual-mode.");
      lcd.setCursor(6,1);
      lcd.print("Don't tag!");

      digitalWrite(buzzerPin, HIGH);
      delay(300);
      digitalWrite(buzzerPin, LOW);
      delay(300);
      digitalWrite(buzzerPin, HIGH);
      delay(300);
      digitalWrite(buzzerPin, LOW);
      delay(00);
    }
  }

  if (mode == true) {
    if (rfid.uid.uidByte[0] != nuidPICC[0] || 
      rfid.uid.uidByte[1] != nuidPICC[1] || 
      rfid.uid.uidByte[2] != nuidPICC[2] || 
      rfid.uid.uidByte[3] != nuidPICC[3] ) {
      Serial.println(F("새로운 인증 시도"));

      saveNuidPICC();

      // changeString();
      uid = dump_byte_array(rfid.uid.uidByte, rfid.uid.size);

      // Serial.print(F("Card_uid:"));
      // Serial.println(uid);

      if (admin.indexOf(uid) != -1) {  
        analogWrite(R_LED, 0);
        analogWrite(G_LED, 255);
        analogWrite(B_LED, 0);
        Serial.println("인증되었습니다.");

        digitalWrite(buzzerPin, HIGH);
        delay(300);
        digitalWrite(buzzerPin, LOW);

        lcd.clear();
        lcd.setCursor(0,0);
        lcd.print("Approved employee");

        if (checkOut == true) {
          flag_print = true;
          
          Serial.print("Out");
          Serial.print(':');
          Serial.println(uid);

          lcd.setCursor(0,1);
          lcd.print("The exit is open");
          servo1.write(90);
          delay(2000);
          servo1.write(0);
          checkOut = false;
        }
        else {
          Serial.print("In");
          Serial.print(':');
          Serial.println(uid);

          lcd.setCursor(0,1);
          lcd.print("Please enter");
          servo1.write(90);
          flag_allow = -1;
          delay(1000);
        }
      }

      else {
        Serial.print("Warning");
        Serial.print(':');
        Serial.println(uid);
        
        analogWrite(R_LED, 255);
        analogWrite(G_LED, 0);
        analogWrite(B_LED, 0);
        Serial.println("권한이 없는 카드입니다.");

        lcd.clear();
        lcd.setCursor(0,0);
        lcd.print("You are not");
        lcd.setCursor(0,1);
        lcd.print("authorized");

        digitalWrite(buzzerPin, HIGH);
        delay(300);
        digitalWrite(buzzerPin, LOW);
        delay(300);
        digitalWrite(buzzerPin, HIGH);
        delay(300);
        digitalWrite(buzzerPin, LOW);
        delay(1000);
      }
    }

    else {
      analogWrite(R_LED, 255);
      analogWrite(G_LED, 165);
      analogWrite(B_LED, 0);
      Serial.println("이미 인증이 진행된 카드입니다.");

      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Duplicate");
      lcd.setCursor(0,1);
      lcd.print("recognized card!");

      digitalWrite(buzzerPin, HIGH);
      delay(300);
      digitalWrite(buzzerPin, LOW);
      delay(300);
      digitalWrite(buzzerPin, HIGH);
      delay(300);
      digitalWrite(buzzerPin, LOW);
      delay(1000);
    }
  }
  lcd.clear();
  analogWrite(R_LED, 0);
  analogWrite(G_LED, 0);
  analogWrite(B_LED, 0);
}

// switch (message) {
//   case "73 bf 0d 12": lcd.setCursor(0,1); lcd.print("kCM");
// }

void saveNuidPICC() {
  for (byte i = 0; i < 4; i++) {
    nuidPICC[i] = rfid.uid.uidByte[i];
  }
}

// HEX 바이트 배열을 String으로 변환하는 함수
void changeString() {
  string_uid = "";
  for (byte i = 0; i < 4; i++) {
    string_uid += String(rfid.uid.uidByte[i], HEX);
    string_uid += " ";
  }
  string_uid = string_uid.substring(0, 10);
}

// HEX 형식 출력 함수
void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

// DEC 형식 출력 함수
void printDec(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], DEC);
  }
}