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
start=time.time()
def read_in_img(filename):
    pixel_values = np.array(image.imread(filename))
    y_max=len(pixel_values)#rows
    x_max=len(pixel_values[0])#columns
    #pixel_values=np.delete(pixel_values,np.s_[y_max-20:y_max],0)
    return pixel_values

def corners_av(pixels,cornersize):
    y_max=len(pixels)#rows
    x_max=len(pixels[0])#columns
    c=cornersize
    t_l=np.average(pixels[0:c,0:c])
    b_l=np.average(pixels[y_max-c:y_max,0:c])
    b_r=np.average(pixels[y_max-c:y_max,x_max-c:x_max])
    t_r=np.average(pixels[0:c,x_max-c:x_max])
    return np.array([t_l,t_r,b_r,b_l])

def grad(corners,pixels):
    y_max=len(pixels)#rows
    x_max=len(pixels[0])#columns
    Upper_grad=(corners[1]-corners[0])/x_max
    left_grad=(corners[3]-corners[0])/x_max
    bottom_grad=(corners[1]-corners[2])/y_max
    right_grad=(corners[3]-corners[2])/y_max
    return np.array([Upper_grad,left_grad,bottom_grad,right_grad])


def read(filename,cornersize):
    
    
    pixels=read_in_img(filename)
    y_max=len(pixels)#rows
    x_max=len(pixels[0])#columns
    '''
    This is needed as imread will not do maths properly on any pixel 
    image reading will now output focal spot with background corrected
    and a metric that correlates to shape of focal spot only
    '''
    pixel_true=np.zeros((len(pixels),len(pixels[0])))#NEEDED AS THIS WILL NOT BE ABLE TO HANDLE MATHS OTHERWISE
    pixel_true[0:len(pixels),0:len(pixels[0])]=pixels[0:len(pixels),0:len(pixels[0])] #NEEDED 
    

    
    corners=corners_av(pixels,cornersize)
    grads=grad(corners,pixels)
    
   
    pixels_coord=np.mgrid[0:y_max,0:x_max].reshape(2,-1).T
    
   
    pixels_coord=(pixels_coord[0:len(pixels_coord),0]*grads[0]+pixels_coord[0:len(pixels_coord),1]*grads[1])+corners[0]
    pixel_background=pixels_coord.reshape(y_max,x_max)
    pixel_true=np.round(pixel_true-pixel_background)
   
    total_pixels=np.sum(pixels)
   
   
    fitness_parameter=np.sum(pixel_true**2)/(total_pixels)
    
    end=time.time()
    print(end-start)
    print(fitness_parameter)
    plt.imshow(pixel_true)
    return fitness_parameter

read('/Users/vedindewan/Desktop/MSci_Project_AO/Focal_Spot_Analysis/Test_Spot_Data/0_0.jpg',6)


#%% Test
list_1=np.zeros((4,4))
list_2=np.array([[0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3],[2,0],[2,1],[2,2],[2,3],[3,0],[3,1],[3,2],[3,3]])

list_2=(list_2[0:len(list_2),0]*2)+(list_2[0:len(list_2),1]*2)
list_1=list_2.reshape(4,4)
print(list_1)





    