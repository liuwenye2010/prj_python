import wave, struct, math

sampleRate = 44100.0 # hertz
duration = 1.0       # seconds
frequency = 440.0    # hertz

wavef = wave.open('sound_mono.wav','w')
wavef.setnchannels(1) # mono
wavef.setsampwidth(2) # 16bits
wavef.setframerate(sampleRate)

for i in range(int(duration * sampleRate)):
    value = int(32767.0*math.cos(frequency*math.pi*float(i)/float(sampleRate)))
    data = struct.pack('<h', value)
    wavef.writeframesraw( data )


wavef.close()