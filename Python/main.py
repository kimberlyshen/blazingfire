import XBee
from time import sleep
import time
import subprocess, shlex
import _thread
import webbrowser

if __name__ == "__main__":
	xbee = XBee.XBee("/dev/tty.usbserial-DA011EDD")
	
sensorValues = [0,0,0,0] 
prediction = False

def machineLearning(threadname):
	while True:
		#pipe = subprocess.Popen(["java", "-classpath", "weka.jar:jython-standalone-2.7-b4.jar","org.python.util.jython","homeMachineLearning.py","home.arff"], stdout=subprocess.PIPE)
		command = "java -classpath weka.jar:jython-standalone-2.7-b4.jar org.python.util.jython homeMachineLearning.py home.arff"
		args = shlex.split(command)
		pipe1 = subprocess.Popen(args, stdout=subprocess.PIPE)
		prediction = pipe1.stdout.read()
		print (bool(prediction))
		print("Done reading")
		pipe1.stdout.close()
		pipe1.kill()

def networkedDevices(threadname):
	while True:
		oldNumDevices = state.numDevices
		pipe = subprocess.Popen(["perl","perl.pl"], stdout=subprocess.PIPE)
		newDeviceNum = pipe.stdout.read()
		pipe.stdout.close()
		pipe.kill()
		res = int(newDeviceNum)
		print(res)
		state.deviceChange = res - oldNumDevices
		state.numDevices = res
		oldNumDevices = res
		print(state.deviceChange)

# enum for sensors
class Sensors:
	Motion, Noise, NumDevices, PeopleCount = range(4)


class State:
	# Threshold for noise sensor
	# boolean occupied
	# boolean motion		# sensorValues[0]
	# int noise				# sensorValues[1]
	# int numDevices 
	# int peopleCount		# sensorValues[2]
	# int deviceChange


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
noise_flag = False;
#f = open('datalog', 'w')
_thread.start_new_thread( machineLearning, ("Thread-2", ) )
_thread.start_new_thread( networkedDevices, ("Thread-1", ) )

while True:
	oldNumDevices = 0
	# A simple string message
	sent = xbee.SendStr("SensorTrue", 0x5678)
	sleep(0.25)
	Msg = xbee.Receive()
	print("Reading motion sensor")
	if Msg:
		content = Msg[7:-1].decode('ascii')
		print("Msg: " + content)
		devA = content.find("Id 1:")
		devB = content.find("Id 2:")
		devC = content.find("Id 3:")
		print("Dev address: " + str(devA))
		print("Dev address: " + str(devB))
		print("Dev address: " + str(devC))

		if devA > 0:
			sensorValue = content.find("True")
			if sensorValues[0] == 0:
				if sensorValue > 0: 
					sensorValues[0] = 1
				else:
					sensorValues[0] = 0
				print(sensorValues); 
		
			state.motion = True if sensorValues[0] == 1 else False

		elif devB > 0:
			sensorValue = content.find("Quie")
			sensorValue2 = content.find("Mode")
			sensorValue3 = content.find("Loud")

			print("sensorValue: " + str(sensorValue))
			print("sensorValue2: " + str(sensorValue2))
			print("sensorValue3: " + str(sensorValue3))

			if sensorValues[1] == 0:
				if sensorValue > 0 and devB > 0:
					sensorValues[1] = 1
				elif sensorValue2 > 0 and devB > 0:
					sensorValues[1] = 2
				elif sensorValue3 > 0 and devB > 0:
					sensorValues[1] = 3
			state.noise = sensorValues[1]

		elif devC >= 0:
			print(content)
			print(content[15])
			if(int(content[15]) > 0):
				state.peopleCount = int(content[15])
				sensorValues[2] = int(content[15])

		print(sensorValues)

	time.sleep(0.25)

	sent = xbee.SendStr("SensorTrue", 0x1994)
	sleep(0.25)

	Msg = xbee.Receive()
	print("Reading noise sensor")
	if Msg:
		content = Msg[7:-1].decode('ascii')
		print("Msg: " + content)
		devA = content.find("Id 1:")
		devB = content.find("Id 2:")
		devC = content.find("Id 3:")
		print("Dev address: " + str(devA))
		print("Dev address: " + str(devB))
		print("Dev address: " + str(devC))

		if devA > 0:
			sensorValue = content.find("True")
			if sensorValues[0] == 0:
				if sensorValue > 0: 
					sensorValues[0] = 1
				else:
					sensorValues[0] = 0
				print(sensorValues)
			if sensorValues[0] == 1:
				state.motion = True
			else:
				state.motion = False
		
		elif devB > 0:
			sensorValue = content.find("Quie")
			sensorValue2 = content.find("Mode")
			sensorValue3 = content.find("Loud")

			print("sensorValue: " + str(sensorValue))
			print("sensorValue2: " + str(sensorValue2))
			print("sensorValue3: " + str(sensorValue3))

			if sensorValues[1] < 3:
				print("Going to change the value")
				if sensorValue > 0 and devB > 0:
					sensorValues[1] = 1
				elif sensorValue2 > 0 and devB > 0:
					sensorValues[1] = 2
				elif sensorValue3 > 0 and devB > 0:
					sensorValues[1] = 3

			
			state.noise = sensorValues[1]
		elif devC >= 0:
			print(content)
			print(content[15])
			if(int(content[15]) > 0):
				state.peopleCount = int(content[15])
				sensorValues[2] = int(content[15])
		print(sensorValues)

	time.sleep(0.25)

	sent = xbee.SendStr("SensorTrue", 0x6677)
	sleep(0.25)
	
	Msg = xbee.Receive()
	print("Reading noise sensor")
	if Msg:
		content = Msg[7:-1].decode('ascii')
		print("Msg: " + content)
		devA = content.find("Id 1:")
		devB = content.find("Id 2:")
		devC = content.find("Id 3:")
		print("Dev address: " + str(devA))
		print("Dev address: " + str(devB))
		print("Dev address: " + str(devC))

		if devA > 0:
			sensorValue = content.find("True")
			if sensorValues[0] == 0:
				if sensorValue > 0: 
					sensorValues[0] = 1
				else:
					sensorValues[0] = 0
			
			if sensorValues[0] == 1:
				state.motion = True
			else:
				state.motion = False
			print(sensorValues)
		elif devB > 0:
			sensorValue = content.find("Quie")
			sensorValue2 = content.find("Mode")
			sensorValue3 = content.find("Loud")

			print("sensorValue: " + str(sensorValue))
			print("sensorValue2: " + str(sensorValue2))
			print("sensorValue3: " + str(sensorValue3))
	
			if sensorValues[1] < 3:
				print("Going to change the value")
				if sensorValue > 0 and devB > 0:
					sensorValues[1] = 1
				elif sensorValue2 > 0 and devB > 0:
					sensorValues[1] = 2
				elif sensorValue3 > 0 and devB > 0:
					sensorValues[1] = 3
			state.noise = sensorValues[1]

		elif devC >= 0:
			print(content)
			print(content[15])
			if(int(content[15]) > 0):
				state.peopleCount = int(content[15])
				sensorValues[2] = int(content[15])

		print(sensorValues)

	time.sleep(0.25)
	
	# need to get networked devices here
	
	# if 30 seconds have passed, run occupancy algorithm
	if(time.time()-start_time > 10):
		counter = 0
		#noise_flag = False
		print(sensorValues)

		# check which sensors are active in order of priority
		counter += 1 if state.motion==True else 0
		counter += 1 if state.noise > NOISE_THRESHOLD else 0
		counter += 1 if state.peopleCount > 0 else 0
		counter += 1 if state.deviceChange > 0 else 0
		counter += 1 if prediction == True else 0

		if (counter >= 2):
			state.occupied = True
			print("Home is occupied. Counter value = " + str(counter))
			sensorString = str(sensorValues)
			resString = 'Data value' + sensorString + '=' + 'Home is occupied'

			print("Sending to the relay now")
			sent = xbee.SendStr("blah", 0x5677)
			sleep(0.25)


		else:
			state.occupied = False
			print("Home is not occupied. Counter value = " + str(counter))
			sensorString = str(sensorValues)
			resString = 'Data value' + sensorString + '=' + 'Home is not occupied'

			print("Sending to the relay now")
			sent = xbee.SendStr("a", 0x5677)
			sleep(0.25)
			

		print("Motion state: " + str(state.motion))
		url = 'http://homeoccupancy-kimberlyshen.c9.io/update_occupancy/' + str(state.occupied) + '/' + str(state.motion) + '/' + str(state.noise) + '/' + str(state.peopleCount) + '/' + str(state.numDevices) + '/'
		print(url)
		webbrowser.open(url)

		print("sensorValues: " + str(sensorValues[0]))
		sensorValues[0] = 0
		sensorValues[1] = 0

		state.motion = False
		state.noise = 0

		time.sleep(1)

		# reset start time to current time
		start_time = time.time()