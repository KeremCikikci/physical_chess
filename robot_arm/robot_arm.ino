int x;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  pinMode(13, OUTPUT);
}

void loop() {
  while (!Serial.available());
  x = Serial.readString().toInt();
  Serial.print(x + 1);

  blink_(x);
}

void blink_(int delay_){
  digitalWrite(13, 1);
  delay(delay_);
  digitalWrite(13, 0);
  delay(delay_);
}
