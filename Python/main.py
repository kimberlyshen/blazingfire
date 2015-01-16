import XBee
from time import sleep

if __name__ == "__main__":
	xbee = XBee.XBee("/dev/tty.usbserial-DA011EDD")
	
	sensorValues = [] 

while True:
	# A simple string message
	sent = xbee.SendStr("SensorTrue", 0x1994)
	sleep(0.25)
	Msg = xbee.Receive()
	if Msg:
		content = Msg[7:-1].decode('ascii')
		print("Msg: " + content)
		sensorValue = content.find("true")
		if sensorValue == 1: 
			sensorValues.insert(0, sensorValue)
		else:
			sensorValues.insert(0, 0);
		print(sensorValues); 

	sent = xbee.SendStr("SensorTrue", 0x5678)
	sleep(0.25)
	Msg = xbee.Receive()
	if Msg:
		content = Msg[7:-1].decode('ascii')
		print("Msg: " + content)
		sensorValue = content.find("true")
		if sensorValue == 1: 
			sensorValues.insert(0, sensorValue)
		else:
			sensorValues.insert(0, 0);
		print(sensorValues);
	
	
	
		

#    # A message that requires escaping
#    xbee.Send(bytearray.fromhex("7e 7d 11 13 5b 01 01 01 01 01 01 01"))
#    sleep(0.25)
#    Msg = xbee.Receive()
#    if Msg:
#        content = Msg[7:-1]
#        print("Msg: " + xbee.format(content))
