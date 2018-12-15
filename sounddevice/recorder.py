#!/usr/bin/env python3
"""Create a recording with arbitrary duration.

PySoundFile (https://github.com/bastibe/PySoundFile/) has to be installed!

"""
import tempfile
import Queue as queue
import sys
import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

class recorder:
    def __init__(self, _folder, _device, _channel):
        self.folder = _folder
        self.device = _device
        device_info = sd.query_devices(self.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        self.samplerate = int(device_info['default_samplerate'])
        self.q = queue.Queue()
        self.channel = _channel


    # est-ce une fonction SELF ???
    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status)
        self.q.put(indata.copy())

    def recordFile(self, filename):
        # Make sure the file is opened before recording anything:
        # check the args.subtype removed
        with sf.SoundFile(filename, mode='x', samplerate=self.samplerate,
                          channels=self.channel ) as file:
            with sd.InputStream(samplerate=self.samplerate, device=self.device,
                                channels=self.channel, callback=self.callback):
                print('#' * 80)
                print('RECORDING')
                print('#' * 80)
                n=0
                while n<450:
                    file.write(self.q.get())
                    n = n+1

    def update(self):

        i= 0
        #Create a real update function to make task independant


