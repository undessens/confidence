from recorder import recorder
from player import player
from arduino import arduino
import os
import time
import threading


def main():

	global rec
	rec = recorder("sound", None ,1)
	play = player("sound", None, 1)

	#GLOBAL STATE
	state = 0
	stories = []

	# IS THERE A FILE AT START
	stories.append(1)
	stories.append(0)
	stories.append(0)
	stories.append(0)
	stories.append(0)
	stories.append(0)
	stories.append(0)
	stories.append(0)

	#ard = arduino("/dev/tty.usbserial-AH06LA61", 115200)
	ard = arduino("/dev/ttyUSB0", 115200)
	ard.connect()

	#THREADING
	run_event = threading.Event()
	run_event.set()


	threadSerial = threading.Thread(target=arduino.loopReadSerial, args=(ard, run_event))
	threadSerial.start()


	#rec.recordFile(nameFile)
	##play the same file
	
	# PLAYER
	# threadPlayer = threading.Thread(target=player.playFile, args=(play, nameFile) )
	# threadPlayer.start()

	#rec.recordFile(nameFile)

	# Wait for arduino to initialize arduino serial 
	time.sleep(4)

	# ard.setLedState(0, 2)
	# ard.setLedState(1, 2)
	# ard.sendLedState()

	# time.sleep(2)

	test = True

	# time.sleep(7)

	print "READY"

	try:
		while True:

			#print "READ buttons"
			if(not(ard.allowRead)):
				for i in range(8) :
					ard.setLedState(i, stories[i]*2)
		 		ard.sendLedState()
		 		ard.allowRead = True

		 	# WAITING
		 	if(state==0):
		 		but = ard.getLastButtonPressed()
		 		
		 		# if (test):
		 		# 	rec.recordFileForIndex(5)
		 		# 	state = 2
		 		# 	test = False

		 		# IF new button
		 		if(but > -1 and but<8):
		 			# IF THERE IS A STORY
		 			if(stories[but]== 1):
		 				play.playFileFromIndex(but)
		 				state = 1
		 			else:
		 				#rec
		 				print "REC"
		 			# 	threadRecorder = threading.Thread(target=rec.recordFileForIndex, args=(rec, but) )
						# threadRecorder.start()
						# print "STARTED"
		 				rec.recordFileForIndex(but)
		 				state = 2

		 	#PLAYING	
		 	elif(state==1):
		 		if(ard.getLastButtonPressed()> -1):
		 			play.stop()
		 			state = 0

		 	#RECORDING
		 	elif(state==2):
		 		print "STOP REC"
		 		index = rec.getLastRecordedIndex()
		 		if(index > -1):
		 			stories[index] = 1
		 		state = 0

		 	
		 	time.sleep(0.1)
	except KeyboardInterrupt:
		play.stop()
		print "killing all thread"
		run_event.clear()
		threadSerial.join()







if __name__ == "__main__":
    main()



