# 센서 및 IoT / 산업 현장 안전 관리 시스템


🧑‍🤝‍🧑 역할 분담

|이름|역할|
|------|--------|
|강민구|시스템 전체에 대한 PyQt 및 DB 관리 시스템 구축|
|김준표|출입문 감지 시스템 및 출입 정보 DB 업데이트 기능 구현|
|김창미|출입문 감지 시스템 및 RFID 기능 구현, PyQt 및 DB 시스템 구축|
|최규호|위험 지역 접근 감지 시스템 아두이노 구현|

## 🖥️ 하드웨어 및 소프트웨어 구성도
![image](https://github.com/changmi-kim/changmi-kim.github.io/assets/141194237/541b7d2d-5997-424f-b829-34d9693344d6)

draw.io 링크: [https://drive.google.com/file/d/1gtUsnsUkhlHpAqQX9k2jctidUJYdlS1m/view?usp=sharing](https://drive.google.com/file/d/1gtUsnsUkhlHpAqQX9k2jctidUJYdlS1m/view?usp=sharing)

## 📊 안전 관리 DB 시스템 순서도
![image](https://github.com/changmi-kim/changmi-kim.github.io/assets/141194237/d29ee2cd-eb3c-45d1-9cda-bb8a99d65fa6)

## ✈️ PPT 자료
https://docs.google.com/presentation/d/1AWp36OybdQL008NTzZpEw1TwQ33S21eg/edit?usp=sharing&ouid=102784698114875004183&rtpof=true&sd=true

## 🏆 프로젝트 소개 
- 최근 정부에서 중대재해법을 제정하였음에도 사고는 계속해서 발생하고 있으며, IoT 기술을 활용하여 안전사고를 방지하는데 도움이 되고자 이번 프로젝트 주제로 선정하게 되었습니다.
- 실제 현장에서 자주 일어나는 안전사고 사례와 현장의 안전팀 등을 본 경험을 토대로 현장에서 효율적으로 사용될 수 있을 기능들을 선정하였습니다.

## 🥇 기능 리스트 
![image](https://github.com/addinedu-ros-3rd/iot-repo-6/assets/87626122/743f2364-f4d6-42f3-ac6f-21d2d068c38b)

## 🥇 위험 지역 접근 감지 스마트 세이프티 센서

![image](https://github.com/addinedu-ros-3rd/iot-repo-6/assets/87626122/ccfea0ac-1966-4220-802d-31033bc0af23)


## 🥇 스마트 출입문 시스템 구성

![image](https://github.com/addinedu-ros-3rd/iot-repo-6/assets/87626122/3ea7efd5-411d-475d-846b-3669c0c9bd82)


## 🥇 PyQt UI 구성

![image](https://github.com/addinedu-ros-3rd/iot-repo-6/assets/87626122/d6cdd2d7-a69d-44de-a100-2c2726581b0c)

## 🥇 스마트 도어 시스템 동작시 DB및 PyQt 업데이트

![image](https://github.com/addinedu-ros-3rd/iot-repo-6/assets/87626122/0c86df78-afea-45de-ae79-167017b12dd2)


## 실행 방법
- arduino_rfid.ino, all_in_one_fuinalalll_ver.ino를 참고하여 아두이노와 포트와 PC 연결

1. 자동 출입 모드
  1. PyQt 우측 하단 '게이트 모드 선택'에서 '자동' 선택
  2. 건물 입장 전 RFID 카드 태그
  3. 바깥쪽 문 앞에 사람이 서면 초음파 센서로 감지하여 문이 열림
  4. 이 후 안쪽 문 앞에 사람이 서면 초음파 센서로 감지하여 문이 열리고 건물 안의 사람 수, 출입 시간, 출입 방향을 DB 및 PyQt에 업데이트
  5. 나갈 때도 같은 방식이며 바깥쪽 문을 나오기 전 카드를 태그하면 문이 열리고 출입 정보 업데이트

2. 수동 출입 모드
  1. PyQt 우측 하단 '게이트 모드 선택'에서 '수동' 선택
  2. 사람이 바깥쪽 문 앞에 서면 카메라로 신원 확인 후 관리자가 PyQt의 open 버튼을 클릭하여 수동으로 열어줌
  3. 이 후 안쪽 문 앞에 사람이 서면 초음파 센서로 감지하여 문이 열리고 건물 안의 사람 수, 출입 시간, 출입 방향을 DB 및 PyQt에 업데이트
  4. 나갈 때도 같은 방식이며 바깥쪽 문을 나오기 전 카메라로 신원 확인 후 관리자가 버튼으로 문을 열어줌
  5. 출입 시 건물 안의 인원 수, 출입 방향, 출입 시간 업데이트





