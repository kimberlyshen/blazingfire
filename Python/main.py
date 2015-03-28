import XBee
from time import sleep
import time
import subprocess, shlex
import _thread
import webbrowser

if __name__ == "__main__":
	xbee = XBee.XBee("/dev/tty.usbserial-DA011EDD")
	
sensorValues = [0,0,0,0] 

def machineLearning(threadname):
	while True:
		#pipe = subprocess.Popen(["java", "-classpath", "weka.jar:jython-standalone-2.7-b4.jar","org.python.util.jython","homeMachineLearning.py","home.arff"], stdout=subprocess.PIPE)
		command = "java -classpath weka.jar:jython-standalone-2.7-b4.jar org.python.util.jython homeMachineLearning.py home.arff"
		args = shlex.split(command)
		print(args)
		print("HELLO")
		pipe = subprocess.Popen(args, stdout=subprocess.PIPE)

		myfile = open("machineLearningPrediction.txt", "r")
		s = myfile.read()
		print(s)
		print("Done reading")
		myfile.close()


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
noise_flag = False;
#f = open('datalog', 'w')
#_thread.start_new_thread( networkedDevices, ("Thread-1", ) )

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
		devAddress = content.find("SensorId 1")
		sensorValue = content.find("True")
		if sensorValue > 0 and devAddress > 0: 
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
	while not (Msg):
		Msg = xbee.Receive()
	
	print("Reading noise sensor")
	if Msg:
		content = Msg[7:-1].decode('ascii')
		print("Msg: " + content)
		
	#	devAddress = content.find("SensorId 2")
    #	print("devAddress" + devAddress);
		sensorValue = content.find("Quie")
		sensorValue2 = content.find("Mode")
		sensorValue3 = content.find("Loud")

		print("sensorValue: " + str(sensorValue))
		print("sensorValue2: " + str(sensorValue2))
		print("sensorValue3: " + str(sensorValue3))
		
		if(noise_flag is False):
			print("noise flag is false")
			if sensorValue > 0:
				sensorValues[1] = 1
			elif sensorValue2 > 0:
				sensorValues[1] = 2
			elif sensorValue3 > 0:
				sensorValues[1] = 3
		else:
			if sensorValues[1] <= 1 and sensorValue > 0:
				sensorValues[1] = 1
			elif sensorValues[1] <= 1 and sensorValue2 > 0:
				sensorValues[1] = 2
			elif sensorValues[1] <= 2 and sensorValue3 > 0:
				sensorValues[1] = 3

		print(sensorValues);
		state.noise = sensorValues[1]

	time.sleep(0.25)
	noise_flag = True

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
		noise_flag = False
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

			print("Sending to the relay now")
			sent = xbee.SendStr("blah", 0x5677)
			sleep(0.25)
			Msg = xbee.Receive()
			if Msg:
				print("Relay got the message")
			print("No response from relay")

			#f.write(resString)
			#_thread.start_new_thread( machineLearning, ("Thread-2", ) )
		else:
			state.occupied = False
			print("Home is not occupied. Counter value = " + str(counter))
			sensorString = str(sensorValues)
			resString = 'Data value' + sensorString + '=' + 'Home is not occupied'

			print("Sending to the relay now")
			sent = xbee.SendStr("a", 0x5677)
			sleep(0.25)
			Msg = xbee.Receive()
			if Msg:
				print("Relay got the message")
			print("No response from relay")
			#f.write(resString)
			#_thread.start_new_thread( machineLearning, ("Thread-2", ) )

		noise_flag = False
		url = 'http://homeoccupancy-kimberlyshen.c9.io/update_occupancy/' + str(state.occupied) + '/' + str(state.motion) + '/' + str(state.noise) + '/' + str(state.peopleCount) + '/' + str(state.numDevices) + '/'
		print(url)
		webbrowser.open(url)
		# should send results to relay module and the web app
		# add logging for state result and time
		myfile = open("home.arff", "a")
		timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		filestr = str(state.occupied) + "," + str(state.motion) + "," + str(state.noise) + "," + str(state.numDevices) + "," + str(state.peopleCount) + "," + str(state.deviceChange) + "\n"
		myfile.write(filestr)
		myfile.close()

		time.sleep(6)

		# reset start time to current time
		start_time = time.time()
#    # A message that requires escaping
#    xbee.Send(bytearray.fromhex("7e 7d 11 13 5b 01 01 01 01 01 01 01"))
#    sleep(0.25)
#    Msg = xbee.Receive()
#    if Msg:
#        content = Msg[7:-1]
#        print("Msg: " + xbee.format(content))
