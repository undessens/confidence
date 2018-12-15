from recorder import recorder
from player import player
from arduino import arduino
import os
import time


def main():

	global rec
	rec = recorder("", None ,1)
	play = player("", None, 1)

	####### MAX OSX
	if os.name == "posix":
		ard = arduino("/dev/tty.usbserial-AH06LA61", 115200)
	####### LINUX
	else:
		ard = arduino("/dev/ttyUSB0", 115200)

	ard.connect()

	print "Welcome"

	#rec.recordFile(nameFile)
	##play the same file
	#play.playFile(nameFile)

	# Wait for arduino to initialize arduino serial 
	time.sleep(2)
	print "GO"


	ard.setLedState(0, 2)
	ard.setLedState(1, 2)
	ard.setLedState(2, 2)
	ard.sendLedState()

	time.sleep(7)

	ard.setLedState(0, 0)
	ard.setLedState(1, 0)
	ard.setLedState(2, 0)
	ard.setLedState(3, 2)
	ard.setLedState(4, 2)
	ard.setLedState(5, 2)
	ard.setLedState(6, 2)
	ard.setLedState(7, 1)
	ard.sendLedState()

	time.sleep(3)

	print "end"





	# while True:

	# 	arduino.readSerial()
	# 	time.sleep(0.1)




if __name__ == "__main__":
    main()



