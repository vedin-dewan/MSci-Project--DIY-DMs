# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 11:32:28 2021

@author: maxim
"""
'''
This works out a gradient to find out background
'''

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
    #pixel_back_ground_x=np.arange(0,601)*grads[0]+corners[0]
    #pixel_back_ground_y=np.arange(0,601)*grads[1]+corners[0]
    #print(pixel_back_ground_x)
    #print(pixel_back_ground_y)
    pixels_coord=np.mgrid[0:601,0:601].reshape(2,-1).T
    pixels_background=np.zeros((601,601))
    #print(pixels_coord)
    #pixel_background=np.array((pixel_back_ground_x,pixel_back_ground_y))
    #print(pixel_background)
    
    
    #print(grads)
   # print(corners)
    #print(pixel_coord[0:601]*grads[0])
    #print(pixel_coord[0:601]*grads[1])
    for i in range(361201):
        #pixel_true[pixels_coord[i][1],pixels_coord[j][1]]-=pixel_background[i
        pixel_true[pixels_coord[i][0],pixels_coord[i][1]]-=(pixels_coord[i][1]*grads[1]+pixels_coord[i][1]*grads[0]+corners[0])
        pixels_background[pixels_coord[i][0],pixels_coord[i][1]]=(pixels_coord[i][0]*grads[1]+pixels_coord[i][1]*grads[0]+corners[0])
 #   for i in range(601):
  #      for j in range(601):
   #         pixel_true[i,j]-=pixel_back_ground_x[i]+pixel_back_ground_y[j]
     #       pixels_background=pixel_back_ground_x[i]+pixel_back_ground_y[j]
    highest_pixel=np.amax(np.ravel(pixels))
    print(pixel_true)
    
    a=np.where(pixels>highest_pixel)
    pixels[a]=0
    total_pixels=np.sum(pixels)
    print(pixels_background)
    print(np.mean(pixels_background))
    '''
    This is needed as imread will not do maths properly on any pixel 
    image reading will now output focal spot with background corrected
    and a metric that correlates to shape of focal spot only
    '''
   
    fitness_parameter=np.sum(pixel_true**2)/(total_pixels)
   # plt.imshow(pixel_true)
    end=time.time()
    print(end-start)
   # print(fitness_parameter)
 
    return fitness_parameter

read('0_0.jpg',6)    
    
    
    
    
    
    
    
    