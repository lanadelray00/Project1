#include <Stepper.h>      // 스테핑 모터 라이브러리

int stepsPerRev = 2048; // 한바퀴(360): 2048

Stepper stepper (stepsPerRev, 11,9,10,8); // ( IN4,IN2,IN3,IN1) 



void setup()

{

  stepper.setSpeed(18);   // 스텝모터의 스피드 설정 최대 18 //최소 1

}

void loop()

{ 

  stepper.step(stepsPerRev);  // 한 바퀴 회전 명령


}