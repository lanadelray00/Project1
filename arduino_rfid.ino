#include <MFRC522.h>
#include <SPI.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <Servo.h>

#define RST_PIN 9
#define SS_PIN 10

Servo servo;
MFRC522 rfid(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;
LiquidCrystal_I2C lcd(0x27, 16, 2);

const int R_LED = A0;
const int G_LED = A1;
const int B_LED = A2; 
const int buzzerPin = A3;

// card_1 73 BF 0D 12
// card_2 C3 61 8E 12
// card_3 A3 C5 C0 12
// card_4 83 03 B8 12

byte nuidPICC[4];
String uid;
String string_uid;

String card_1 = "73 bf 0d 12";
String card_2 = "c3 61 8e 12";
String card_3 = "a3 c5 c0 12";
String card_4 = "83 03 b8 12";

String admin = "73 bf 0d 12, c3 61 8e 12";  // 승인된 카드 uid
String not_admin = "a3 c5 c0 12, 83 03 b8 12";  // 승인되지 않은 카드 uid

void setup() {
  Serial.begin(9600);
  pinMode(buzzerPin, OUTPUT);
  servo.attach(6);
  
  SPI.begin();

  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }

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
  lcd.setCursor(0,0);
  lcd.print("Please tag");
  lcd.setCursor(0,1);
  lcd.print("your employee ID");

  if ( ! rfid.PICC_IsNewCardPresent())
    return;

  if ( ! rfid.PICC_ReadCardSerial())
    return;

  if (rfid.uid.uidByte[0] != nuidPICC[0] || 
    rfid.uid.uidByte[1] != nuidPICC[1] || 
    rfid.uid.uidByte[2] != nuidPICC[2] || 
    rfid.uid.uidByte[3] != nuidPICC[3] ) {
    Serial.println(F("새로운 인증 시도"));

    saveNuidPICC();

    // changeString();
    uid = dump_byte_array(rfid.uid.uidByte, rfid.uid.size);

    Serial.print(F("Card_uid:"));
    Serial.println(uid);

    if (admin.indexOf(uid) != -1) {
      analogWrite(R_LED, 0);
      analogWrite(G_LED, 255);
      analogWrite(B_LED, 0);
      Serial.println("인증되었습니다.");

      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Approved employee");
      lcd.setCursor(0,1);
      lcd.print("Please enter");

      digitalWrite(buzzerPin, HIGH);
      delay(300);
      digitalWrite(buzzerPin, LOW);

      servo.write(180);
      delay(2000);
      servo.write(0);
    }

    else {
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

  lcd.clear();
  analogWrite(R_LED, 0);
  analogWrite(G_LED, 0);
  analogWrite(B_LED, 0);
}

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