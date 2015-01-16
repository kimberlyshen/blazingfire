import XBee
from time import sleep

if __name__ == "__main__":
	xbee = XBee.XBee("/dev/tty.usbserial-DA011EDD")

class State:
	boolean occupied
	boolean motion # sensorValues[0]
	boolean noise  # sensorValues[1]
	int numDevices # sensorValues[2]
	int peopleCount

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

while True:
	# A simple string message
	sent = xbee.SendStr("SensorTrue", 0x1994)
	sleep(0.25)
	Msg = xbee.Receive()
	if Msg:
		content = Msg[7:-1].decode('ascii')
		print("Msg: " + content)

	sent = xbee.SendStr("SensorTrue", 0x5678)
	sleep(0.25)
	Msg = xbee.Receive()
	if Msg:
		content = Msg[7:-1].decode('ascii')
		print("Msg: " + content)
		
		
		

#    # A message that requires escaping
#    xbee.Send(bytearray.fromhex("7e 7d 11 13 5b 01 01 01 01 01 01 01"))
#    sleep(0.25)
#    Msg = xbee.Receive()
#    if Msg:
#        content = Msg[7:-1]
#        print("Msg: " + xbee.format(content))
