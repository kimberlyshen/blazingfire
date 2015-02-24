import XBee
from time import sleep
import time
import subprocess
import _thread

if __name__ == "__main__":
	xbee = XBee.XBee("/dev/tty.usbserial-DA011EDD")
	
sensorValues = [0,0,0,0] 

def networkedDevices(threadname):
	while True:
		pipe = subprocess.Popen(["perl","perl.pl"], stdout=subprocess.PIPE)
		newDeviceNum = pipe.stdout.read()
		pipe.stdout.close()
		pipe.kill()
		res = int(newDeviceNum)
		print(res)
		state.deviceChange = res - oldNumDevices
		print(state.deviceChange)
		print("I am running bitch! I am the thread!!!! ")

# enum for sensors
class Sensors:
	Motion, Noise, NumDevices, PeopleCount = range(4)


class State:
	# Threshold for noise sensor
	#boolean occupied
	#boolean motion		# sensorValues[0]
	#int noise		# sensorValues[1]
	#int numDevices 
	#int peopleCount		# sensorValues[2]
	#int deviceChange


	def __init__(self, occupied=False, motion=False, noise="Quiet", numDevices=0, peopleCount=0, deviceChange=0):
		self.occupied = False
		self.motion = False
		self.noise = 1
		self.numDevices = 0
		self.peopleCount = 0
		self.deviceChange = 0
	
	def printState(self):
		print ("Occupied:          " + self.occupied)
		print ("Motion:            " + self.motion)
		print ("Noise:             " + self.noise)
		print ("Connected Devices: " + self.numDevices)
		print ("People Count:      " + self.peopleCount)
		print ("DeviceChange:	  " + self.deviceChange)
	
# Instantiate the State object
state = State()
start_time = time.time()
NOISE_THRESHOLD = 1

#f = open('datalog', 'w')
_thread.start_new_thread( networkedDevices, ("Thread-1", ) )

while True:
	oldNumDevices = state.numDevices
	
	
	# A simple string message
	sent = xbee.SendStr("SensorTrue", 0x5678)
	sleep(0.25)
	Msg = xbee.Receive()
	print('Trying to read motion sensor')
	if Msg:
		content = Msg[7:-1].decode('ascii')
		print("Msg: " + content)
		sensorValue = content.find("True")
		if sensorValue > 0: 
			sensorValues[0] = 1
		else:
			sensorValues[0] = 0
		print(sensorValues); 
		state.motion = True if sensorValues[0] == 1 else False
		print(sensorValues)
		
		
	time.sleep(0.25)

	sent = xbee.SendStr("SensorTrue", 0x1994)
	sleep(0.25)
	Msg = xbee.Receive()
	if Msg:
		content = Msg[7:-1].decode('ascii')
		print("Msg: " + content)
		
		print("Got message from noise sensor")
		
		sensorValue = content.find("Quie")
		sensorValue3 = content.find("Mode")
		sensorValue2 = content.find("Loud")
		
		if sensorValue > 0:
			sensorValues[1] = 1
		elif sensorValue2 > 0:
			sensorValues[1] = 2
		elif sensorValue3 > 0:
			sensorValues[1] = 3

		print(sensorValues);
		state.noise = sensorValues[1]

				
#		sensorValue = content.find("sensor1true")
#		sensorValue2 = content.find("sensor2true")
#		
#		if sensorValue == 1: 
#			sensorValues.insert(1, sensorValue)
#		else:
#			sensorValues.insert(1, 0)
#		print(sensorValues)
#		
#		if sensorValue2 == 1: 
#			sensorValues.insert(1, sensorValue2)
#		else:
#			sensorValues.insert(1, 0)
#		print(sensorValues)
#				
#		
	
#	# need to get networked devices here
	

	# if 30 seconds have passed, run occupancy algorithm
	if(time.time()-start_time > 10):
		counter = 0
		
		print(sensorValues)
		
	#	pipe = subprocess.Popen(["perl","perl.pl"], stdout=subprocess.PIPE)
	#	newDeviceNum = pipe.stdout.read()
	#	pipe.stdout.close()
	#	pipe.kill()
	#	res = int(newDeviceNum)
	#	print(res)
	#	state.deviceChange = res - oldNumDevices
	#	print(state.deviceChange)

		# check which sensors are active in order of priority
		counter += 1 if state.motion==True else 0
		counter += 1 if state.noise > NOISE_THRESHOLD else 0
#		counter += 1 if state.peopleCount > 0 else 0
		counter += 1 if state.deviceChange > 0 else 0
#		
		if (counter >= 2):
			state.occupied = True
			print("Home is occupied. Counter value = " + str(counter))
			sensorString = str(sensorValues)
			resString = 'Data value' + sensorString + '=' + 'Home is occupied'
			f.write(resString)
		else:
			state.occupied = False
			print("Home is not occupied. Counter value = " + str(counter))
			sensorString = str(sensorValues)
			resString = 'Data value' + sensorString + '=' + 'Home is not occupied'
			f.write(resString)

#		# should send results to relay module and the web app
#		# add logging for state result and time
        with open("home.arff", "a") as myfile:
            myfile.write(state.occupied + "," + state.motion + "," + state.noise + "," + state.numDevices + "," + state.peopleCount + "," + state.deviceChange + "," time.localtime())
            print(time.localtime())
            myfile.close()
                    
		time.sleep(6)
#
		# reset start time to current time
		start_time = time.time()
#		

#    # A message that requires escaping
#    xbee.Send(bytearray.fromhex("7e 7d 11 13 5b 01 01 01 01 01 01 01"))
#    sleep(0.25)
#    Msg = xbee.Receive()
#    if Msg:
#        content = Msg[7:-1]
#        print("Msg: " + xbee.format(content))
