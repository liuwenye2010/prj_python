import wave, struct, math

sampleRate = 44100.0 # hertz
duration = 1.0       # seconds

freq = 880.00  # A
maxVolume = 32767.0

wavef = wave.open('sound_volume.wav','w')
wavef.setnchannels(1) # stereo
wavef.setsampwidth(2) 
wavef.setframerate(sampleRate)

nSamples = duration * sampleRate
for i in range(int(nSamples)):
    volume = maxVolume*float(i)/nSamples
    a = int(volume*math.cos(freq*math.pi*float(i)/float(sampleRate)))
    wavef.writeframesraw( struct.pack('<h', a ) )

wavef.writeframes('')
wavef.close()