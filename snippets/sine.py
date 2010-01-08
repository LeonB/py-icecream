# create a synthetic 'sine wave' wave file with set frequency and length
# tested with Python25 and Python30  by vegaseat  28dec2008

import math
import wave
import struct

def make_soundfile(freq=440, data_size=10000, filename="sine_wave1.wav"):
    """
    create a synthetic 'sine wave' wave file with frequency freq
    file has a length of about data_size*2 and the given filename
    """
    frate = 11025.0  # framerate as a float
    amp = 8000.0     # multiplier for amplitude

    # make a sine list ...
    sin_list = []
    for i in range(data_size):
        sin_list.append(math.sin(2*math.pi*freq*(i/frate)))
    wav_file = wave.open(filename, "w")

    # required parameters ...
    nchannels = 1
    sampwidth = 2
    framerate = int(frate)
    nframes = size
    comptype = "NONE"
    compname = "not compressed"

    # set all the parameters at once
    wav_file.setparams((nchannels, sampwidth, framerate, nframes,
        comptype, compname))

    # now write out the file
    print("may take a few seconds ...")
    for s in sin_list:
        # write the audio frames, make sure nframes is correct
        wav_file.writeframes(struct.pack('h', s*amp/2))
    wav_file.close()
    print( "%s written" % filename)


# set some variables ...
freq = 0.0
size = 30000  # data size, file size will be about twice that

# write the synthetic wave file to ...
filename = "WaveTest2.wav"

make_soundfile(freq, size, filename)