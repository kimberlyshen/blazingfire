import XBee
from time import sleep
import time

if __name__ == "__main__":
	xbee = XBee.XBee("/dev/tty.usbserial-DA011EDD")
	
sensorValues = [] 

# enum for sensors
class Sensors:
	Motion, Noise, NumDevices, PeopleCount = range(4)

class State:
	boolean occupied
	boolean motion # sensorValues[0]
	boolean noise  # sensorValues[1]
	int numDevices 
	int peopleCount # sensorValues[2]


	def __init__(self):
		self.occupied = False
		self.motion = False
		self.noise = False
		self.num_devices = 0
		self.peopleCount = 0
	
	def printState(self):
		print "Occupied:          %s" % State.occupied
		print "Motion:            %s" % State.motion
		print "Noise:             %s" % State.noise
		print "Connected Devices: %d" % State.numDevices
		print "People Count:      %d" % State.peopleCount

// Instantiate the State object
state = State()
start_time = time.time()

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
		state.motion = sensorValues[0]

	sent = xbee.SendStr("SensorTrue", 0x5678)
	sleep(0.25)
	Msg = xbee.Receive()
	if Msg:
		content = Msg[7:-1].decode('ascii')
		print("Msg: " + content)
		sensorValue = content.find("true")
		if sensorValue == 1: 
			sensorValues.insert(1, sensorValue)
		else:
			sensorValues.insert(1, 0)
		print(sensorValues)
		
		state.noise = sensorValues[1]

	# if 30 seconds have passed, run occupancy algorithm
	if(time.time()-start_time > 30):
		int sensor = -1
		
		# check which sensors are active in order of priority
		if(state.motion):
			sensor = Sensors.Motion
		elseif(state.noise):
			sensor = Sensors.Noise
		elseif(state.peopleCount > 0):
			sensor = Sensors.PeopleCount
		elseif(state.numDevices > 0):
			sensor = Sensors.NumDevices

		# call function

		# add logging for state result and time

		# reset start time to current time
		start_time = time.time()
		

#    # A message that requires escaping
#    xbee.Send(bytearray.fromhex("7e 7d 11 13 5b 01 01 01 01 01 01 01"))
#    sleep(0.25)
#    Msg = xbee.Receive()
#    if Msg:
#        content = Msg[7:-1]
#        print("Msg: " + xbee.format(content))
