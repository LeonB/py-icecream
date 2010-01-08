import wave
#w = wave.Wave_write(None)
#print dir(w.struct)
w = wave.open('test.wav', 'w')
w.setnchannels(1)
w.setsampwidth(4)
w.setframerate(44100)
w.setnframes(100000)