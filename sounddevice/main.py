from recorder import recorder
from player import player
from arduino import arduino
import os
import time
import threading


def main():

	global rec
	rec = recorder("", None ,1)
	play = player("", None, 1)


	#ard = arduino("/dev/tty.usbserial-AH06LA61", 115200)
	ard = arduino("/dev/ttyUSB0", 115200)
	ard.connect()
	threadSerial = threading.Thread(target=arduino.loopReadSerial, args=([ard]) )
	threadSerial.start()

	print("Welcome")
	nameFile = "truc5.wav"
	#rec.recordFile(nameFile)
	##play the same file
	
	# PLAYER
	# threadPlayer = threading.Thread(target=player.playFile, args=(play, nameFile) )
	# threadPlayer.start()

	
	play.playFile(nameFile)

	#rec.recordFile(nameFile)

	# Wait for arduino to initialize arduino serial 
	time.sleep(2)

	ard.setLedState(0, 2)
	ard.setLedState(1, 2)
	ard.setLedState(2, 2)
	ard.sendLedState()
	# time.sleep(7)

	while True:

		#print "loop"
		if(not(ard.allowRead)):
	 		ard.sendLedState()
	 		ard.allowRead = True
	 	
	 	time.sleep(0.1)






if __name__ == "__main__":
    main()



