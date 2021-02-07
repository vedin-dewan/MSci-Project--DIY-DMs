#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 13:07:52 2021

@author: maximillianstunt & vedindewan 
"""
"""
This works out a gradient)both x and y dirn) to find out background
Then finds fitness parameter for focal spot by squaring pixel values
and normalising to total pixel value.
"""

import numpy as np
from matplotlib import image
import time
import matplotlib.pyplot as plt

def read_in_img(filename):
    pixel_values = np.array(image.imread(filename))
    return pixel_values

def corners_av(pixels,cornersize):
    c=cornersize
    t_l=np.average(pixels[0:c,0:c])
    b_l=np.average(pixels[601-c:601,0:c])
    b_r=np.average(pixels[601-c:601,601-c:601])
    t_r=np.average(pixels[0:c,601-c:601])
    return np.array([t_l,t_r,b_r,b_l])

def grad(corners):
    Upper_grad=(corners[1]-corners[0])/601
    left_grad=(corners[3]-corners[0])/601
    bottom_grad=(corners[1]-corners[2])/601
    right_grad=(corners[3]-corners[2])/601
    return np.array([Upper_grad,left_grad,bottom_grad,right_grad])


def read(filename,cornersize):
    start=time.time()
    pixels=read_in_img(filename)
    '''
    This is needed as imread will not do maths properly on any pixel 
    image reading will now output focal spot with background corrected
    and a metric that correlates to shape of focal spot only
    '''
    pixel_true=np.zeros((len(pixels),len(pixels[0])))#NEEDED AS THIS WILL NOT BE ABLE TO HANDLE MATHS OTHERWISE
    pixel_true[0:len(pixels),0:len(pixels[0])]=pixels[0:len(pixels),0:len(pixels[0])] #NEEDED 
    

    
    corners=corners_av(pixels,cornersize)
    grads=grad(corners)
    pixel_background=np.zeros((601,601))
   
    pixels_coord=np.mgrid[0:601,0:601].reshape(2,-1).T
   
    
    pixel_background[0:601,0:601]=(pixels_coord[0:601,0]*grads[1]+pixels_coord[0:601,1]*grads[0])+corners[0] 
    pixel_true=np.round(pixel_true-pixel_background)
   
    total_pixels=np.sum(pixels)
   
   
    fitness_parameter=np.sum(pixel_true**2)/(total_pixels)
    
    end=time.time()
    print(end-start)
    print(fitness_parameter)
    #plt.imshow(pixel_true)
    return fitness_parameter

read('/Users/vedindewan/Desktop/MSci_Project_AO/Focal_Spot_Analysis/Test_Spot_Data/0_0.jpg',6)    