import Queue as queue
import sounddevice as sd
import soundfile as sf

class player:
	def __init__(self, _folder, _device, _channel):
		self.folder = _folder
		self.device = _device
		device_info = sd.query_devices(self.device, 'input')
		# soundfile expects an int, sounddevice provides a float:
		self.samplerate = int(device_info['default_samplerate'])
		self.channel = _channel
		self.buffersize = 25
		self.blocksize = 2048

		# Transport attribute
		self.isPlaying = False

		# Fonctionna attribute
		self.q = queue.Queue(maxsize=self.buffersize)


	def callback(self, outdata, frames, time, status):
		assert frames == self.blocksize
		if status.output_underflow:
		    print('Output underflow: increase blocksize?')
		    raise sd.CallbackAbort
		assert not status
		try:
		    data = self.q.get_nowait()
		except queue.Empty:
		    print('Buffer is empty: increase buffersize?')
		    raise sd.CallbackAbort
		if len(data) < len(outdata):
		    outdata[:len(data)] = data
		    outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
		    raise sd.CallbackStop
		else:
		    outdata[:] = data

	def end(self):
		print "End of playing file"
		self.isPlaying = False

	def playFile(self, filename):

		self.isPlaying = True
		print('#' * 80)
		print('PLAYING')
		print('#' * 80)

		with sf.SoundFile(filename) as f:
			for _ in range(self.buffersize):
				data = f.buffer_read(self.blocksize, ctype='float')
				if not data:
				    break
				self.q.put_nowait(data)  # Pre-fill queue

			stream = sd.RawOutputStream(
				samplerate=self.samplerate, blocksize=self.blocksize,
				device=self.device, channels=self.channel, dtype='float32',
				callback=self.callback, finished_callback=self.end)
			with stream:
			    timeout = self.blocksize * self.buffersize / f.samplerate
			    while data:
			        data = f.buffer_read(self.blocksize, ctype='float')
			        self.q.put(data, timeout=timeout)
			    event.wait()  # Wait until playback is finished

