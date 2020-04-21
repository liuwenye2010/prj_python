
import wave, struct, math
def packSoundFrame(nChannels,sampleWidth,values):
    """Returns a packed structure that you can write to a wave file.
   nChannels -- 1 for mono, 2 for stereo, etc...
   sampleWidth -- size of data: 1 = 8 bits, 2 = 16, 3 = invalid, 4 = 32, etc...
   values -- array of floats between -1.0 and +1.0

   packSound(2,2,[-0.5,1.0])"""

    formats = (None,'B','h',None,'l')
    offsets = (None,127, 0, None,0)

    format = formats[sampleWidth]*nChannels
    offset = offsets[sampleWidth] 
    volume = 2**(8*sampleWidth-1) - 1

    args = [format]
    for value in values:
        args.append(int(offset + volume*value)) 

    return struct.pack( *args )
	

sampleRate = 44100.0 # hertz
duration = 1.0       # seconds
lFreq =  880.00        # A
rFreq = 1760.00        # A

# 8 bit stereo sound
sampleWidth = 1
nChannels = 2

wavef = wave.open('sound.wav','w')
wavef.setnchannels(nChannels) # stereo
wavef.setsampwidth(sampleWidth)
wavef.setframerate(sampleRate)

nSamples = duration * sampleRate
for i in range(int(nSamples)):
    l = math.cos(lFreq*math.pi*float(i)/float(sampleRate))
    r = math.cos(rFreq*math.pi*float(i)/float(sampleRate))
    data = packSoundFrame(nChannels, sampleWidth, [l,r])
    wavef.writeframesraw( data )

wavef.writeframes('')
wavef.close()