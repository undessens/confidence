import serial

class arduino:

	def __init__(self, _port, _baudrate):
		self.port = _port
		self.baudrate = _baudrate
		# Num of channels, led and buttons
		self.numButtons = 8
		
		#Buttons state
		self.buttonState = []

		self.ledState = []

		self.initState()

		self.s  =  None

	def initState(self):

		print "Init state"

		for i in range(self.numButtons) :
			self.buttonState.append(False)
		
		for i in range(self.numButtons) :
			self.ledState.append(0)

		print self.buttonState
		print self.ledState

	def connect(self):

		try :
			self.s = serial.Serial(self.port, self.baudrate)
			print "connected"
		except :
			print "***impossible de se connecter"







	def readSerial(self):

		bytye = ''
		byte = self.s.read(1)
		newValue = []

		for i in range(0, numButtons):
			self.newValue[i] = byte & (1<<i)

		for i in range(0, self.numButtons):
			
			# Button is pressed
			if( self.newValue[i] and not(self.buttonState[i])):
				self.buttonPressed(i)


			#update values
			self.buttonState[i] = newValue[i]

	def buttonPressed(self, index):

		print "buttonPressed : "+str(index)


	def sendLedState(self):

		msg = ""

		for i in range(0, self.numButtons):
			msg += chr(self.ledState[i] + 48 )

		msg += 'A'
		self.s.write(msg)
		print "message send : "+msg

	def setLedState( self, index , state): 

		if(index>=0 and index<self.numButtons ):
			if(state >=0 and state < 3):
				self.ledState[index] = state

		print "ledState modified"
		print self.ledState














