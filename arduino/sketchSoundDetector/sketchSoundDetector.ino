/******************************************************************************
 *
 * For more details about the Sound Detector, please check the hookup guide.
 *
 * Connections:
 * The Sound Detector is connected to the Adrduino as follows:
 * (Sound Detector -> Arduino pin)
 * GND → GND
 * VCC → 5V
 * Gate → Pin 2
 * Envelope → A0
 * 
 * Resources:
 * Additional library requirements: none
 * 
 * Development environment specifics:
 * Using Arduino IDe 1.0.5
 * Tested on Redboard, 3.3v/8MHz and 5v/16MHz ProMini hardware.
 * 
 * This code is beerware; if you see me (or any other SparkFun employee) at the
 * local, and you've found our code helpful, please buy us a round!
 * 
 * Distributed as-is; no warranty is given.
 ******************************************************************************/
#include "XBee.h"
#include "queue.h"
#include <SoftwareSerial.h>

XBee xbee;
Queue RxQ;
SoftwareSerial sserial(12,13);

 // Define hardware connections
#define PIN_GATE_IN 2
#define IRQ_GATE_IN  0
#define PIN_LED_OUT 13
#define PIN_ANALOG_IN A0

// soundISR()
// This function is installed as an interrupt service routine for the pin
// change interrupt.  When digital input 2 changes state, this routine
// is called.
// It queries the state of that pin, and sets the onboard LED to reflect that 
// pin's state.
void soundISR()
{
  int pin_val;

  pin_val = digitalRead(PIN_GATE_IN);
  digitalWrite(PIN_LED_OUT, pin_val);   
}

void setup()
{
  Serial.begin(9600);
  sserial.begin(9600);
  //  Configure LED pin as output
  pinMode(PIN_LED_OUT, OUTPUT);

  // configure input to interrupt
  pinMode(PIN_GATE_IN, INPUT);
  attachInterrupt(IRQ_GATE_IN, soundISR, CHANGE);

  // Display status
  Serial.println("Initialized");
}

void loop()
{
  int value;
  String result;
  // Check the envelope input
  value = analogRead(PIN_ANALOG_IN);

  // Convert envelope value into a message
  Serial.print("Status: ");
  if(value <= 3)
  {
    Serial.println("Quiet.");
    result = "Quiet";
  }
  else if( (value > 3) && ( value <= 10) )
  {
    Serial.println("Moderate.");
    result = "Moderate";
  }
  else if(value > 10)
  {
    Serial.println("Loud.");
    result = "Loud";
  }
  
  
  delay(5);
    int queueLen = 0;
    int delPos = 0;
   
    while (sserial.available() > 0){
        unsigned char in = (unsigned char)sserial.read();
        Serial.println("Received");
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
                if(result == "Quiet") {
                  memcpy(outMsg, "SensorId 2: Quie", 16);
                } else if (result == "Moderate") {
                  memcpy(outMsg, "SensorId 2: Mode", 16);
                } else {                  
                  memcpy(outMsg, "SensorId 2: Loud", 16);
                }
                
                // len - (9 bytes of frame not in message content)
            //    memcpy(&outMsg[10], &msgBuff[8], msgLen-9);
                
                Serial.println(outMsg[2]);
                // 10 + (-9) = 1 more byte in new content than in previous message
                frameLen = xbee.Send(outMsg, 16, outFrame, addr);
                Serial.println("Sent packet");
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

  // pause for 1 second
  delay(1000);
}
