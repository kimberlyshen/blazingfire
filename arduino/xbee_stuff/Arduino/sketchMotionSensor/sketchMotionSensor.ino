#include "XBee.h"
#include "queue.h"
#include <SoftwareSerial.h>

/////////////////////////////
//VARS
//the time we give the sensor to calibrate (10-60 secs according to the datasheet)
int calibrationTime = 30;        

int pirPin = 2;    //the digital pin connected to the PIR sensor's output
int ledPin = 13;

XBee xbee;
Queue RxQ;
SoftwareSerial sserial(12,13);


/////////////////////////////
//SETUP
void setup(){
  Serial.begin(9600);
  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(pirPin, LOW);
 
    sserial.begin(9600);

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
  int isMotion = 0;

  if(pirVal == LOW){ //was motion detected
    Serial.println("Motion detected at home");
    isMotion = 1;
   
    
    delay(500); 
  }
    else{
    Serial.println("Motion not detected at home"); 
    isMotion = 0;
    delay(500); 
  }
  
  if(isMotion == 1){
    
    delay(5);
    int queueLen = 0;
    int delPos = 0;
   
    while (sserial.available() > 0){
        unsigned char in = (unsigned char)sserial.read();
        if (!RxQ.Enqueue(in)){
            break;
        }
    }

    queueLen = RxQ.Size();
    for (int i=0;i<queueLen;i++){
        if (RxQ.Peek(i) == 0x7E){
            unsigned char checkBuff[Q_SIZE];
            unsigned char msgBuff[Q_SIZE];
            int checkLen = 0;
            int msgLen = 0;

            checkLen = RxQ.Copy(checkBuff, i);
            msgLen = xbee.Receive(checkBuff, checkLen, msgBuff);
            if (msgLen > 0){
                unsigned char outMsg[Q_SIZE];
                unsigned char outFrame[Q_SIZE];
                int frameLen = 0;
            //    int addr = ((int)msgBuff[4] << 8) + (int)msgBuff[5];
                int addr = 1;
                Serial.println(addr);
                Serial.println(msgLen);
                // 10 is length of "you sent: "
                memcpy(outMsg, "SensorId 1: True", 16);
                // len - (9 bytes of frame not in message content)
            //    memcpy(&outMsg[10], &msgBuff[8], msgLen-9);
                
                Serial.println(outMsg[2]);
                // 10 + (-9) = 1 more byte in new content than in previous message
                frameLen = xbee.Send(outMsg, 16, outFrame, addr);
                sserial.write(outFrame, frameLen);
                i += msgLen;
                delPos = i;    
            }else{
                if (i>0){
                    delPos = i-1;
                }
            }
        }
    }

    RxQ.Clear(delPos); 
  }
  

}
