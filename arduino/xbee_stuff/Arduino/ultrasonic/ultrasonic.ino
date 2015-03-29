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

int counter = 0;
int first, second = 0;
int dist_one, dist_two = 0;
int people_count = 0;


/////////////////////////////
//SETUP
void setup(){
  Serial.begin(9600);
  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(pirPin, LOW);
 
    sserial.begin(9600);
    
   pinMode (2,INPUT);//attach pin 2 to door contact sensor
  // initialize serial communication:
  Serial.begin(9600);


}





void loop(){

  dist_one = getDistance(3,4);
  Serial.println("Distance 1: ");
  Serial.println(dist_one);
  
  if(dist_one < 10 && dist_one != 0){
    while(getDistance(3,4) < 10){
      Serial.println("Looping");
      if(getDistance(3,4) == 0)
      break;
    }
    
    Serial.println("Someone walked out");
    delay(300);
    people_count--;
  }
  else if(dist_one == 0){
   Serial.println("Out of range"); 
  }
  
  Serial.println(people_count);
  

  dist_two = getDistance(6,7);
  Serial.println("Distance 2: ");
  Serial.println(dist_two);
    if(dist_two < 10 && dist_two != 0){
    while(getDistance(6,7) < 10){
      Serial.println("Looping");
      if(getDistance(6,7) == 0)
      break;
    }
    
    Serial.println("Someone walked in");
    people_count++;
        delay(300);
  }
  else if(dist_two == 0){
   Serial.println("Out of range"); 
  }
  
  Serial.println(people_count);
  if( people_count < 1){
    people_count = 0;
  }
  
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
                String msg_str = "SensorId 3: Tru";
                msg_str += people_count;
                
                Serial.println(msg_str);
               
                
                for ( int i = 0; i < msg_str.length(); i++){    
                    outMsg[i] = msg_str[i];
                    Serial.println(outMsg[i]);
                }
                outMsg[msg_str.length()] = '/0';
                
                
              //  memcpy(outMsg, ptr , 16);
                
              //  Serial.println(outMsg);
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



long getDistance(int trig, int echo){
  
  // establish variables for duration of the ping,
  // and the distance result in inches and centimeters:
  long duration, inches, cm, distance;
  int currentState = 0;
  int previousState = 0;

  // The PING))) is triggered by a HIGH pulse of 2 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  
  pinMode(trig, OUTPUT);// attach pin 3 to Trig
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(5);
  digitalWrite(trig, LOW);

  // The same pin is used to read the signal from the PING))): a HIGH
  // pulse whose duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode (echo, INPUT);//attach pin 4 to Echo
  duration = pulseIn(echo, HIGH);

  // convert the time into a distance
  inches = microsecondsToInches(duration);
  cm = microsecondsToCentimeters(duration);
  distance = (duration/2) / 29.1;
  
  return distance;
  
  
  
}

long microsecondsToInches(long microseconds)
{
  // According to Parallax's datasheet for the PING))), there are
  // 73.746 microseconds per inch (i.e. sound travels at 1130 feet per
  // second).  This gives the distance travelled by the ping, outbound
  // and return, so we divide by 2 to get the distance of the obstacle.
  // See: http://www.parallax.com/dl/docs/prod/acc/28015-PING-v1.3.pdf
  return microseconds / 74 / 2;
}

long microsecondsToCentimeters(long microseconds)
{
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the
  // object we take half of the distance travelled.
  return microseconds / 29 / 2;
}
