from recorder import recorder
from player import player
import time
import serial

def main():

	global rec
	rec = recorder("", None ,1)
	play = player("", None, 1)

	ser = serial.Serial('/dev/tty.usbserial', 9600)
	
	time.sleep(1)
	print "start recording"

	##chose record file name that doesn't exist
	nameFile = "truc6.wav"

	
	rec.recordFile(nameFile)

	##play the same file
	play.playFile(nameFile)



if __name__ == "__main__":
    main()



