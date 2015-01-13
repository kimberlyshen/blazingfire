#include <avr/sleep.h>

int Door_Led_Pin = 13;   // choose the pin for the LED
int Door_Sensor_Pin = 2; // choose the Door_Sensor_Pin
int val = 0;             // variable for reading the Door_Sensor_Pin status
 
void setup() {
  pinMode(Door_Led_Pin, OUTPUT);    // declare Door_Led_Pin as output
  pinMode(Door_Sensor_Pin, INPUT);  // declare Door_Sensor_Pin as input
  attachInterrupt(0, transmitDoorState, CHANGE);
  Serial.begin(9600);
}

void transmitDoorState() {
  int door = digitalRead(Door_Sensor_Pin);  // read Door_Sensor_Pin
  
  // If Door_Sensor N.C. (no with magnet) -> HIGH : Door is open / LOW : Door is closed 
  // If Door_Sensor N.0. (nc with magnet) -> HIGH : Door is closed / LOW : Door is open [This will be our case in AHA Project]
  if (door == HIGH) {         
    digitalWrite(Door_Led_Pin, LOW);  //Set Door_Led low
    Serial.println("closed");
  } else {
    digitalWrite(Door_Led_Pin, HIGH);  //Set Door_Led high
    Serial.println("open");
  }
  
  delay(100);
}

void loop(){
  set_sleep_mode(SLEEP_MODE_IDLE);
  sleep_enable();
  sleep_mode();
}
