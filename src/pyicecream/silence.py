import math
import wave
import array

class Silence(object):
    samplerate = 44100
    length = 3
    frequency = 400
    channels = 1 #don't know if this works correctly

    def data(self):
        sin = math.sin
        pi = math.pi
        twopi = 2*pi

        data = array.array('h')

        num_samples = self.length * self.samplerate

        cycles_per_sample = float(self.frequency/self.channels)/self.samplerate

        volume_scale = (.85)*32767

        for samp in xrange(num_samples):
            phi = samp * cycles_per_sample
            phi -= int(phi)
            data.append(int(round(volume_scale * sin(twopi * phi))))

        return data.tostring()

    def write(self, file):
        f = wave.open(file, 'w')
        f.setparams((self.channels, 2, self.samplerate, 0, "NONE", "Uncompressed"))
        f.writeframes(self.data())
        f.close()
        return f