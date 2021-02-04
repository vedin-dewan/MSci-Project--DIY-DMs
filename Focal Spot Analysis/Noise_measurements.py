# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:50:04 2021

@author: maxim
"""

import numpy as np
from matplotlib import image
import time
import matplotlib.pyplot as plt

image_1='0_0.jpg'
image_2='0_1.jpg'
image_3='849_2631_2325_920_817.jpg'
image_4='893_2386_2339_973_1003.jpg'
image_5='1168_1630_1922_640_1493.jpg'
image_6='1163_1300_2061_703_1901.jpg'
image_7='1191_1416_1850_873_1261.jpg'
image_8='1377_2150_2261_513_501.jpg'
image_9='1282_2143_2022_755_606.jpg'
image_10='1178_2192_2173_666_277.jpg'
images=[image_1,image_2,image_3,image_4,image_5,image_6,image_7,image_8,image_9,image_10]
mean_pixles=[]

def read_in_img(filename):
    pixel_values = np.array(image.imread(filename))
    mean_pixles.append(np.mean(pixel_values))
    
    return pixel_values



def corner_noise(filename,cornersize,position_x,position_y):
    pixels=read_in_img(filename)
    c=cornersize
    p_x=position_x
    p_y=position_y
    t_l=np.average(pixels[p_x:c+p_x,p_y:c+p_y])
    b_l=np.average(pixels[601-c-p_x:601-p_x,p_y:c+p_y])
    b_r=np.average(pixels[601-c-p_x:601-p_x,601-c-p_y:601-p_y])
    t_r=np.average(pixels[p_x:c+p_x,601-c-p_y:601-p_y])
    return np.array([t_l,b_l,b_r,t_r])

def noise(filename,c):
    t_r_noises=[]
    t_l_noises=[]
    b_r_noises=[]
    b_l_noises=[]
    for i in range(0,10,2):
        t_r_noises.append(np.round(corner_noise(filename,c,0,i)[3]))
        t_l_noises.append(np.round(corner_noise(filename,c,0,i)[0]))
        b_r_noises.append(np.round(corner_noise(filename,c,0,i)[2]))
        b_l_noises.append(np.round(corner_noise(filename,c,0,i)[1]))
    for j in range(0,10,2):
        t_r_noises.append(np.round(corner_noise(filename,c,i,0)[3]))
        t_l_noises.append(np.round(corner_noise(filename,c,i,0)[0]))
        b_r_noises.append(np.round(corner_noise(filename,c,i,0)[2]))
        b_l_noises.append(np.round(corner_noise(filename,c,i,0)[1]))
    
   # print('right bottom background averages')    
    #print(b_r_noises)
    means=np.zeros(4)  
    std=np.zeros(4)
    std[0]=np.std(t_r_noises)
    means[0]=np.mean(t_r_noises)
    std[1]=np.std(b_r_noises)
    means[1]=np.mean(b_r_noises)
    std[2]=np.std(b_l_noises)
    means[2]=np.mean(b_l_noises)
    std[3]=np.std(t_l_noises)
    means[3]=np.mean(t_l_noises)
    percentage_std=np.zeros(4)
    #print('standard deviation and mean')
    #print(std)
    #print(means)
    for i in range(len(means)):
        if means[i] == 0 :
            percentage_std[i]=0
        else:
            percentage_std[i]=(std[i]/means[i])*100
    average_noise=np.mean(percentage_std)
    average_mean=np.mean(means)
    print(average_noise)
    print(percentage_std)
    return average_noise,average_mean



for j in range(len(images)):
    noises=[]
    cornersizes=np.arange(4,25,1)
    for i in range(4,25,1):
        noises.append(noise(images[j],i)[0])

    plt.figure(1)        
    plt.plot(cornersizes,noises,label='images%i'%j)
    plt.legend()
    plt.xlabel('Corner box length')
    plt.ylabel('Standard deviation')

# for j in range(len(images)):
#     averages=[]
#     cornersizes=np.arange(4,300,1)
#     for i in range(4,300,1):
#         averages.append(noise(images[j],i)[1])
#     plt.figure(1)
#     plt.plot(cornersizes,averages,label='images%i' %j)
#     plt.legend()
#     plt.xlabel('Corner box length')
#     plt.ylabel('averages of pixel values in boxes')
    
#%%

mean_pixels=[]
image_1='0_0.jpg'
image_2='0_1.jpg'
image_3='849_2631_2325_920_817.jpg'
image_4='893_2386_2339_973_1003.jpg'
image_5='1168_1630_1922_640_1493.jpg'
image_6='1163-1300_2061_703_1901.jpg'
image_7='1191_1416_1850_873_1261.jpg'
image_8='1377_2150_2261_513_501.jpg'
image_9='1282_2143_2022_755_606.jpg'
image_10='1178_2191_2173_666_277.jpg'
images=[image_1,image_2,image_3,image_4,image_5]

def read_in_img(filename):
    pixel_values = np.array(image.imread(filename))
    mean_pixels.append(np.mean(pixel_values))
    
    return pixel_values

for i in range(len(images)):
    read_in_img(images[i])
print(mean_pixels)



    