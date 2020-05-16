#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os 
import sys 
import re 
import glob 
import numpy as np 
#import lxml 
#import requests 
import matplotlib.pyplot as plt 

def  demo_numpy():
    array1= np.array([1,2,3,4])
    print(array1)
    array1 = np.array([[1,  2],  [3,  4]])  # 
    print (array1)

    a = np.arange(24)  
    #print (a.ndim)             # a 现只有一个维度
    print (a)
    # 现在调整其大小
    b = a.reshape(2,4,3)  # b 现在拥有三个维度
    #print (b.ndim)
    print(b)

    # 数组的 dtype 为 int8（一个字节）  
    x = np.array([1,2,3,4,5], dtype = np.int8)  
    print (x.itemsize)
    
    # 数组的 dtype 现在为 float64（八个字节） 
    y = np.array([1,2,3,4,5], dtype = np.float64)  
    print (y.itemsize)

    a = np.arange(6).reshape(2,3)
    for x in np.nditer(a.T):
        print (x, end=", " )
    print ('\n')
    
    for x in np.nditer(a.T.copy(order='C')):
        print (x, end=", " )
    print ('\n')




    a = np.array([1,2,3,4,5]) 
    # 保存到 outfile.npy 文件上
    np.save('outfile.npy',a) 
    b = np.load('outfile.npy')  
    print (b)

    a = np.array([1,2,3,4,5]) 
    np.savetxt('out.txt',a) 
    b = np.loadtxt('out.txt') 

    a=np.arange(0,10,0.5).reshape(4,-1)
    np.savetxt("out2.txt",a,fmt="%d",delimiter=",") # 改为保存为整数，以逗号分隔
    b = np.loadtxt("out2.txt",delimiter=",") # load 时也要指定为逗号分隔
    print(b)


    # 计算正弦曲线上点的 x 和 y 坐标
    x = np.arange(0,  3  * np.pi,  0.1) 
    y = np.sin(x)
    plt.title("sine wave form")  
    # 使用 matplotlib 来绘制点
    plt.plot(x, y) 
    plt.show()

    pass 


def main():
    demo_numpy()
    pass 

if __name__ == "__main__":
    main()
    pass
