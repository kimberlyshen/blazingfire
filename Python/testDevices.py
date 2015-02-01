import subprocess

# need to get networked devices here
pipe = subprocess.Popen(["perl","perl.pl"], stdout=subprocess.PIPE)
newDeviceNum = pipe.stdout.read()
pipe.stdout.close()
pipe.kill()
print("Number of Devices: "+ newDeviceNum)