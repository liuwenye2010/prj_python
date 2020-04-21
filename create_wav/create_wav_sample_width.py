import wave, struct, math

sampleRate = 44100.0 # hertz
duration = 1.0       # seconds

sampleWidth = 1

freq = 880.00  # A
maxVolume = 2**(8*sampleWidth-1) - 1
print str(maxVolume)

wavef = wave.open('sound_sample_width.wav','w')
wavef.setnchannels(1) # stereo
wavef.setsampwidth(sampleWidth)
wavef.setframerate(sampleRate)

nSamples = duration * sampleRate
for i in range(int(nSamples)):
    volume = maxVolume*float(i)/nSamples
    a = int(127+volume*math.cos(freq*math.pi*float(i)/float(sampleRate)))
    wavef.writeframesraw( struct.pack('<B', a ) )

wavef.writeframes('')
wavef.close()