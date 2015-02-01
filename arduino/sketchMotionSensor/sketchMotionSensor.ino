
/////////////////////////////
//VARS
//the time we give the sensor to calibrate (10-60 secs according to the datasheet)
int calibrationTime = 30;        

int pirPin = 2;    //the digital pin connected to the PIR sensor's output
int ledPin = 13;


/////////////////////////////
//SETUP
void setup(){
  Serial.begin(9600);
  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(pirPin, LOW);

  //give the sensor some time to calibrate
  Serial.print("Calibrating PIR motion sensor ");
    for(int i = 0; i < calibrationTime; i++){
      Serial.print(".");
      delay(1000);
      }
    Serial.println(" done");
    Serial.println("SENSOR ACTIVE");
    delay(50);
  }





void loop(){
  int pirVal = digitalRead(pirPin);

  if(pirVal == HIGH){ //was motion detected
    Serial.println("Motion detected at home"); 
    delay(500); 
  }
    else{
    Serial.println("Motion not detected at home"); 
    delay(500); 
  }
  

}
