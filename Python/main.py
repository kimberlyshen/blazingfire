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
	# Threshold for noise sensor
	int NOISE_THRESHOLD = 0
	boolean occupied
	boolean motion		# sensorValues[0]
	int noise		# sensorValues[1]
	int numDevices 
	int peopleCount		# sensorValues[2]
	int deviceChange


	def __init__(self):
		self.occupied = False
		self.motion = False
		self.noise = 0
		self.num_devices = 0
		self.peopleCount = 0
		self.deviceChange = 0
	
	def printState(self):
		print "Occupied:          %s" % self.occupied
		print "Motion:            %s" % self.motion
		print "Noise:             %d" % self.noise
		print "Connected Devices: %d" % self.numDevices
		print "People Count:      %d" % self.peopleCount
		print "DeviceChange:	  %d" % self.deviceChange
	
// Instantiate the State object
state = State()
start_time = time.time()

while True:
	int oldNumDevices = state.numDevices

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
		state.motion = True if sensorValues[0] == 1 else False

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
	
	# need to get networked devices here
	# int newDeviceNum = CALL PERL SCRIPT
	# state.deviceChange = newDeviceNum - oldNumDevices

	# if 30 seconds have passed, run occupancy algorithm
	if(time.time()-start_time > 30):
		int counter = 0

		# check which sensors are active in order of priority
		counter += 1 if state.motion else 0
		counter += 1 if state.noise > NOISE_THRESHOLD else 0
		counter += 1 if state.peopleCount > 0 else 0
		counter += 1 if state.deviceChange > 0 else 0
		
		if (counter >= 3):
			state.occupied = True
			print("Home is occupied. Counter value = %d") % counter
		else:
			state.occupied = False
			print("Home is not occupied. Counter value = %d") % counter

		# should send results to relay module and the web app
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
