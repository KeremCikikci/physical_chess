#include <Servo.h>
Servo w;

#define dsP A5
#define latchP A4
#define clockP 13
#define button 11

#define gripper 8

#define dirX  6
#define pulseX 7
#define switchX A3
#define dirY 5
#define pulseY 12
#define switchY A1
#define dirZ  2
#define pulseZ 10
#define switchZ A2

boolean rotX = false; // false: autohome
boolean rotY = true; // false: autohome
boolean rotZ = true; // false: autohome

double SPMX = 10.1;//9.5; // 9.75, 8.5
double SPDY = 28.89;//28.89
double SPDZ = 28.89;

double posX;
double angleA = 0;
double angleB = 0;
double angleC = 90;

int squaresA[8];
int squaresB[8];

int servoBost = 10;

int aAngles_[8][2] = {{110, 87}, {105, 79}, {95, 72}, {85, 64}, {78, 60}, {65, 52}, {57, 46}, {52, 38}};
int bAngles_[8][2] = {{24, 30}, {40, 43}, {55, 55}, {70, 68}, {80, 78}, {90, 90}, {105, 103}, {119, 116}};
int servoBosts[8] = {20, 18, 17, 12, 12, 10, 8, 10};
String alphabet[8] = {"h", "g", "f", "e", "d", "c", "b", "a"};

String move_ = "None";
String capture_ = "None";
String first, second, third, fourth;
int num1, num2;
double squareSize = 40;
double rightPadding = 40;

String data;

unsigned int digits[8] = {32927, 16421, 8205, 4249, 2121, 1089, 539, 257};/*{0, 0, 0, 0, 0, 0, 0, 0};*/

String strBinDig;
String clock_;
String message;

String firstClock;
String secondClock;

boolean turn = true;

unsigned long previousMillis = 0;
const unsigned long interval = 1000;

String segments[10] = {
  "0000001", // 0
  "1001111", // 1
  "0010010", // 2
  "0000110", // 3
  "1001100", // 4
  "0100100", // 5
  "0100000", // 6
  "0001111", // 7
  "0000000", // 8
  "0000100"  // 9
};


void autoHome(int delay_){
  w.write(120);
  rotX = false; // false: autohome
  rotY = false; // false: autohome
  rotZ = false; // false: autohome

  boolean switchXValue;
  boolean switchYValue;
  boolean switchZValue;
  
  digitalWrite(dirX, rotX);
  digitalWrite(dirY, rotY);
  digitalWrite(dirZ, rotZ);

  for(int i = 0; i < (int)(30 * SPDY); i++){
    switchYValue = digitalRead(switchY);
    digitalWrite(pulseY, 1);
    delayMicroseconds(delay_);
    digitalWrite(pulseY, 0);
    delayMicroseconds(delay_);

    if (switchYValue == 1)
      break;
  }
  
  while (true){
    switchXValue = digitalRead(switchX);
    switchYValue = digitalRead(switchY);
    switchZValue = digitalRead(switchZ);
    
    if (switchXValue == 0)
      digitalWrite(pulseX, 1);
      
    if (switchYValue == 0)
      digitalWrite(pulseY, 1);
    
    if (switchZValue == 0)
      digitalWrite(pulseZ, 1);
    
    delayMicroseconds(delay_);
    if (switchXValue == 0)
      digitalWrite(pulseX, 0);
    
    if (switchYValue == 0)
      digitalWrite(pulseY, 0);
    
    if (switchZValue == 0)
      digitalWrite(pulseZ, 0);
    
    if ((switchXValue == 1) && (switchYValue == 1) && (switchZValue == 1)){
      posX = 0;
      angleA = 127.2;//143.3
      angleB = 119;//108
      angleC = 90;

      break;
    }
    delayMicroseconds(delay_);
  }
  w.write(90);
}

int findMax(int a, int b, int c) {
  int maxVal = a;

  if (b > maxVal) {
    maxVal = b;
  }

  if (c > maxVal) {
    maxVal = c;
  }

  return maxVal;
}

void goPos(double xPosToGo, double aAngleToGo, double bAngleToGo, int minSpeed, int maxSpeed, int servoBost = 0){
  double deltaPosX = posX - xPosToGo;
  double deltaAngleA = angleA - aAngleToGo;
  double deltaAngleB = angleB - bAngleToGo;
  
  double posX_ = posX;
  double angleA_ = angleA;
  double angleB_ = angleB;
  
  int stepsX = abs(deltaPosX * SPMX);
  int stepsA = abs(deltaAngleA * SPDY);
  int stepsB = abs(deltaAngleB * SPDZ);

  int maxStep = findMax(stepsX, stepsA, stepsB);
  
  int steppedX = 0;
  int steppedA = 0;
  int steppedB = 0;
  
  double steppedAngleA = 0;
  double steppedAngleB = 0;

  rotX = true;
  rotY = false;
  rotZ = false;

  if (deltaPosX > 0)
    rotX = false;
  if (deltaAngleA > 0)
    rotY = true;
  if (deltaAngleB > 0)
    rotZ = true;

  digitalWrite(dirX, rotX);
  digitalWrite(dirY, rotY);
  digitalWrite(dirZ, rotZ);
    
  int phrase = 1;
  
  int lengthOfPhrase1 = maxStep/3;
  int lengthOfPhrase3 = maxStep/3;
  
  int delay_;

  int counter = 0;
  
  while (true){
    unsigned long currentMillis = millis();
    
    boolean switchXValue = digitalRead(switchX);
    boolean switchYValue = digitalRead(switchY);
    boolean switchZValue = digitalRead(switchZ);
/*
    if (((switchXValue == 1) || (switchYValue == 1) || (switchZValue == 1)) && (counter > 2000)){
      autoHome(500);
      break;
    }*/

    if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    if (turn == false){
      firstClock = String(firstClock.toInt()-1);
      int zeros = 4 - firstClock.length();
      for (int i = 0; i < zeros; i++){
        firstClock = "0" + firstClock;
      }
    }
    else{
      secondClock = String(secondClock.toInt()-1);
      int zeros = 4 - secondClock.length();
      for (int i = 0; i < zeros; i++){
        secondClock = "0" + secondClock;
      }
    }
    clock_ = formatTime(firstClock.toInt()) + formatTime(secondClock.toInt());
    formatClock();
  }
  
    counter++;
    
    stepsX--;
    stepsA--;
    stepsB--;

    if ((steppedX > maxStep - lengthOfPhrase3) || (steppedA > maxStep - lengthOfPhrase3) || (steppedB > maxStep - lengthOfPhrase3))
      phrase = 3;
    else if ((steppedX > lengthOfPhrase1) || (steppedA > lengthOfPhrase1) || (steppedB > lengthOfPhrase1))
      phrase = 2;

    if (phrase == 3)
      delay_ = map(counter, maxStep - lengthOfPhrase3, maxStep, maxSpeed, minSpeed);
    if (phrase == 2)
      delay_ = maxSpeed;
    if (phrase == 1)
      delay_ = map(counter, 0, lengthOfPhrase1, minSpeed, maxSpeed);
    
    if (stepsX >= 0){
      digitalWrite(pulseX, 1); 
    }
       
    if (stepsA >= 0){
      digitalWrite(pulseY, 1);
    }
      
    if (stepsB >= 0){
      digitalWrite(pulseZ, 1);
    }
      
    delayMicroseconds(delay_);

    if (stepsX >= 0){
      digitalWrite(pulseX, 0);
      steppedX++;
    }
    if (stepsA >= 0){
      digitalWrite(pulseY, 0);
      steppedA++;
    }
    if (stepsB >= 0){
      digitalWrite(pulseZ, 0);
      steppedB++;
    }
    
    if ((stepsX < 0) && (stepsA < 0) && (stepsB < 0)){
      posX = xPosToGo;
      angleA = aAngleToGo;
      angleB = bAngleToGo;
      
      break;
    }

    steppedAngleA = steppedA / SPDY;
    steppedAngleB = steppedB / SPDZ;

    if (rotX == false)
      posX = posX + steppedX;
    else
      posX = posX - steppedX;
      
    if (rotY == false)
      angleA = angleA_ + steppedAngleA;
    else
      angleA = angleA_ - steppedAngleA;

    if (rotZ == false)
      angleB = angleB_ + steppedAngleB;
    else
      angleB = angleB_ - steppedAngleB;

    angleC = 270 - angleA - angleB;

    if ((angleC > 60) && (angleC < 160))
      w.write(angleC + servoBost);
      //Serial.println(angleC);
    delayMicroseconds(delay_);
  }
  posX = xPosToGo;
  angleA = aAngleToGo;
  angleB = bAngleToGo;
}

int findIndexOfChar(String str, String target) {
  int strLength = str.length();
  int targetLength = target.length();
  
  for (int i = 0; i <= strLength - targetLength; i++) {
    if (str.substring(i, i + targetLength) == target) {
      return i; // Eğer hedef string bulunursa indeksi döndür
    }
  }
  
  return -1;
}
int findIndexOfStringInList(String list[], String targetString) {
  for (int i = 0; i < 8; i++) {
    if (list[i] == targetString) {
      return i; // String karakterini içeren stringin indeksini döndür
    }
  }
  return -1; // String karakterini içeren string bulunamazsa -1 döndür
}
void formatClock(){
  for (int i = 0; i < clock_.length(); i++) {
        // pre 0 s
        for (int pre0s = 0; pre0s < i; pre0s++){
          strBinDig.concat("0");
        }
        // 1
        strBinDig.concat("1");
        // post 0 s
        for (int post0s = 0; post0s < clock_.length() - i - 1; post0s++){
          strBinDig.concat("0");
        }
        strBinDig.concat(segments[clock_.charAt(i) - '0']);
        // point
        if ((i == 1) || (i == 5)){
          strBinDig.concat("0");
        }
        else{
          strBinDig.concat("1");
        }
        long decDig = strtol(strBinDig.c_str(), NULL, 2);
        digits[i] = decDig;
        strBinDig = "";
      }
}

String formatTime(unsigned int totalSeconds) {
  unsigned int minutes = totalSeconds / 60;
  unsigned int seconds = totalSeconds % 60;

  String formattedTime = "";

  if (minutes < 10) {
    formattedTime += "0";
  }
  formattedTime += String(minutes);

  if (seconds < 10) {
    formattedTime += "0";
  }
  formattedTime += String(seconds);

  return formattedTime;
}

void setup(){
  pinMode(dsP, OUTPUT);
  pinMode(latchP, OUTPUT);
  pinMode(clockP, OUTPUT);
  pinMode(button, INPUT);
  
  pinMode(dirX, OUTPUT);
  pinMode(pulseX, OUTPUT);
  pinMode(switchX, INPUT);
  pinMode(dirY, OUTPUT);
  pinMode(pulseY, OUTPUT);
  pinMode(switchY, INPUT);
  pinMode(dirZ, OUTPUT);
  pinMode(pulseZ, OUTPUT);
  pinMode(switchZ, INPUT);
  pinMode(gripper, OUTPUT);
  w.attach(9);
  digitalWrite(gripper, 0);

  Serial.begin(115200);
  Serial.setTimeout(1);
  digitalWrite(dirX, rotX);
  digitalWrite(dirY, rotY);
  digitalWrite(dirZ, rotZ);/*
  for(int i = 0; i < (int)(SPDY * 100); i++){
    digitalWrite(dirY, 1);
    digitalWrite(pulseY, 1);
    delayMicroseconds(500);
    digitalWrite(pulseY, 0);
    delayMicroseconds(500);
  }*/
/*
  for(int i = 0; i < (int)(SPDZ * 360); i++){
    digitalWrite(dirZ, 1);
    digitalWrite(pulseZ, 1);
    delayMicroseconds(500);
    digitalWrite(pulseZ, 0);
    delayMicroseconds(500);
  }*/
  autoHome(500);
  digitalWrite(gripper,0);
  goPos(0, 90, 90, 1000, 400, 0);
}


void loop(){
  unsigned long currentMillis = millis();
  
  if (digitalRead(button) == 0)
      Serial.println("move");
      
  if (Serial.available() > 0){
    delay(100);
    if (Serial.available() > 0){
      data =  Serial.readStringUntil('\n');
      Serial.println("O");
      // clock
      if (data.length() == 8){
        if (turn == true)
          turn = false;
        else
          turn = true;
        
        firstClock = data.substring(0, 4);
        secondClock = data.substring(4);
        clock_ = formatTime(firstClock.toInt()) + formatTime(secondClock.toInt());
        Serial.println(clock_);
        formatClock();
      }
      // hamleyi gönder
      // castles
      else if (data == "S"){
        // ilk kare 
        digitalWrite(gripper, 0);
        goPos(20 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1000, 400, servoBosts[0]);
        digitalWrite(gripper, 1);
        delay(250);
        goPos(20 + rightPadding, aAngles_[0][1], bAngles_[0][1], 1800, 1200, servoBosts[0]);
        delay(250);
        goPos(20 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1800, 1200, servoBosts[0]);
        delay(250);
        
        // ucuncu kare
        goPos(100 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1000, 400, servoBosts[0]);
        delay(250);
        goPos(100 + rightPadding, aAngles_[0][1], bAngles_[0][1], 1800, 1200, servoBosts[0]);
        digitalWrite(gripper, 0);
        delay(250);
        goPos(100 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1800, 1200, servoBosts[0]);
        delay(250);

        // dördüncü kare
        goPos(140 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1000, 400, servoBosts[0]);
        digitalWrite(gripper, 1);
        delay(250);
        goPos(140 + rightPadding, aAngles_[0][1], bAngles_[0][1], 1800, 1200, servoBosts[0]);
        delay(250);
        goPos(140 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1800, 1200, servoBosts[0]);
        delay(250);
        
        // ikinci kare
        goPos(60 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1000, 400, servoBosts[0]);
        delay(250);
        goPos(60 + rightPadding, aAngles_[0][1], bAngles_[0][1], 1800, 1200, servoBosts[0]);
        digitalWrite(gripper, 0);
        delay(250);
        goPos(60 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1800, 1200, servoBosts[0]);
        delay(250);

        goPos(0, 90, 90, 1000, 400, 0);
      }

      else if (data == "L"){
        // 4. kare 
        digitalWrite(gripper, 0);
        goPos(140 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1000, 400, servoBosts[0]);
        digitalWrite(gripper, 1);
        delay(250);
        goPos(140 + rightPadding, aAngles_[0][1], bAngles_[0][1], 1800, 1200, servoBosts[0]);
        delay(250);
        goPos(140 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1800, 1200, servoBosts[0]);
        delay(250);
        
        // 6. kare
        goPos(220 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1000, 400, servoBosts[0]);
        delay(250);
        goPos(220 + rightPadding, aAngles_[0][1], bAngles_[0][1], 1800, 1200, servoBosts[0]);
        digitalWrite(gripper, 0);
        delay(250);
        goPos(220 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1800, 1200, servoBosts[0]);
        delay(250);

        // 8. kare
        goPos(300 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1000, 400, servoBosts[0]);
        digitalWrite(gripper, 1);
        delay(250);
        goPos(300 + rightPadding, aAngles_[0][1], bAngles_[0][1], 1800, 1200, servoBosts[0]);
        delay(250);
        goPos(300 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1800, 1200, servoBosts[0]);
        delay(250);
        
        // 5. kare
        goPos(180 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1000, 400, servoBosts[0]);
        delay(250);
        goPos(180 + rightPadding, aAngles_[0][1], bAngles_[0][1], 1800, 1200, servoBosts[0]);
        digitalWrite(gripper, 0);
        delay(250);
        goPos(180 + rightPadding, aAngles_[0][0], bAngles_[0][0], 1800, 1200, servoBosts[0]);
        delay(250);

        goPos(0, 90, 90, 1000, 400, 0);
      }
      
      else if (((data == "M") && (move_ != "None")) || ((data == "C") && (move_ != "None"))){
        num1 = second.toInt() - 1;
        num2 = fourth.toInt() - 1;

        // 1. Yukarda
        double x1 = findIndexOfStringInList(alphabet, first) * squareSize + squareSize / 2 + rightPadding;
        int y1 = num1;
        double a1Y = aAngles_[y1][0];
        double b1Y = bAngles_[y1][0];

        // 1. Assada
        double a1A = aAngles_[y1][1];
        double b1A = bAngles_[y1][1];

        // 2. Yukarda
        double x2 = findIndexOfStringInList(alphabet, third) * squareSize + squareSize / 2 + rightPadding;
        int y2 = num2;
        double a2Y = aAngles_[y2][0];
        double b2Y = bAngles_[y2][0];

        // 2. Assada
        double a2A = aAngles_[y2][1];
        double b2A = bAngles_[y2][1];
        
        // Harakete gec
        // tas yenirse
        if (data == "C"){
          // 2. Tasin üstüne git
          digitalWrite(gripper, 0);
          goPos(x2, a2Y, b2Y, 1000, 400, servoBosts[y2 ]);
          delay(250);
          digitalWrite(gripper, 1);

          // 2. i al
          goPos(x2, a2A, b2A, 1800, 1200, servoBosts[y2 ]);
          delay(250);
          goPos(x2, a2Y, b2Y, 1800, 1200, servoBosts[y2 ]);
          delay(250);

          // kenara at
          goPos(0, 65, 90, 1000, 400, 0);
          delay(250);
          digitalWrite(gripper, 0);
        }
        
        // 1. Tasin üstüne git
        digitalWrite(gripper, 0);
        delay(250);
        goPos(x1, a1Y, b1Y, 1000, 400, servoBosts[y1 ]);
        delay(250);

        // 1. Tasi al
        digitalWrite(gripper, 1);
        delay(250);
        goPos(x1, a1A, b1A, 1800, 1000, servoBosts[y1 ]);
        delay(250);
        goPos(x1, a1Y, b1Y, 1800, 1000, servoBosts[y1 ]);
        delay(250);

        // 2. Tasin üstüne git
        goPos(x1 - (x1 - x2)/2, a2Y+10, b2Y-5, 1000, 400, servoBosts[y2 ]);
        goPos(x2, a2Y, b2Y, 1000, 400, servoBosts[y2 ]);
        delay(250);
        
        // 2. Tasi birak;
        goPos(x2, a2A, b2A, 1800, 1000, servoBosts[y2 ]);
        delay(250);
        digitalWrite(gripper, 0);
        delay(1000);
        goPos(x2, a2Y+2, b2Y+1, 1800, 1000, servoBosts[y2 ]);
        delay(250);
        goPos(0, 90, 90, 600, 400, 0);
        delay(250);
        
        
        move_ = "None";
      }
      
      // hamleyi cek
      else if (data.length() == 4){
        move_ = data;

        first = move_.substring(0, 1);
        second = move_.substring(1, 2);
        third = move_.substring(2, 3);
        fourth = move_.substring(3, 4);
      }
    }
  }
  for (int i = 0; i < 8; i++){
    byte lowLED  = lowByte(digits[i]);
    byte highLED = highByte(digits[i]);
    
    digitalWrite(latchP, 0);
    
    shiftOut(dsP, clockP, LSBFIRST, lowLED);
    shiftOut(dsP, clockP, LSBFIRST, highLED);
    
    digitalWrite(latchP, 1);
    delay(2);
  }
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    if (turn == false){
      firstClock = String(firstClock.toInt()-1);
      int zeros = 4 - firstClock.length();
      for (int i = 0; i < zeros; i++){
        firstClock = "0" + firstClock;
      }
    }
    else{
      secondClock = String(secondClock.toInt()-1);
      int zeros = 4 - secondClock.length();
      for (int i = 0; i < zeros; i++){
        secondClock = "0" + secondClock;
      }
    }
    clock_ = formatTime(firstClock.toInt()) + formatTime(secondClock.toInt());
    formatClock();
  }
}
