#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os 
import sys 
import getopt
import wave as we
import numpy as np
import matplotlib.pyplot as plt

def demo_parse_wave_using_binary_read():
    #读取wav前四个字节内容  -xlxw
    file = open("ARROW.WAV", "rb")
    s = file.read(4)
    print(s)
    #读取wav前44个字节内容  -xlxw
    s = file.read(44)
    print(s)

def wavread(path):
    '''
    读取一个wav文件，返回声音信号的时域谱矩阵和播放时间
    '''
    wavfile =  we.open(path,"rb")
    params = wavfile.getparams()
    framesra,frameswav= params[2],params[3]
    datawav = wavfile.readframes(frameswav)
    num_frame = wavfile.getnframes() # 获取帧数
    num_channel  = wavfile.getnchannels() 
    num_sample_width =  wavfile.getsampwidth() #即每一帧的字节数
    framerate= wavfile.getframerate()
    wavfile.close()
    datause = np.fromstring(datawav,dtype = np.short)
    datause.shape = -1,2
    datause = datause.T
    time = np.arange(0, frameswav) * (1.0/framesra) # # 计算声音的播放时间，单位为秒
    return datause,time

def main():
    #path = input("The Path is:")
    path=r'./ARROW.WAV'
    wavdata,wavtime = wavread(path)
    plt.title("ARROW.wav's Frames")
    plt.subplot(211)
    plt.plot(wavtime, wavdata[0],color = 'green')
    plt.subplot(212)
    plt.plot(wavtime, wavdata[1])
    plt.show()

 
if __name__ == "__main__":
    #demo_parse_wave_using_binary_read()
    main()
    pass