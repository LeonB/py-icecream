import math
import wave
import array

sin = math.sin
pi = math.pi
twopi = 2*pi

data = array.array('h')

sampleRate = 44100 #44100 Samples per Second
length = 3 #3 Seconds

numSamples = length * sampleRate

freq = 2000
cyclesPerSample = float(freq)/sampleRate

volumeScale = (.85)*32767

for samp in xrange(numSamples):
    phi = samp * cyclesPerSample
    phi -= int(phi)

    data.append(int(round(volumeScale * sin(twopi * phi))))

f = wave.open('sinWave.wav', 'w')
f.setparams((1, 2, sampleRate, 0, "NONE", "Uncompressed"))
f.writeframes(data.tostring())
f.close()