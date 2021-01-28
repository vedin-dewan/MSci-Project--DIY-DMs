# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 16:15:04 2021

@author: maxim
"""

#To measure corners of the focal spot

import numpy as np
from matplotlib import image
import time
import matplotlib.pyplot as plt

#%%
def read_in_img(filename):
    pixel_values = np.array(image.imread(filename))
    #pixel=np.ravel(pixel_values)
    return pixel_values

def corners_av(filename,cornersize):
    pixels=read_in_img(filename)
    c=cornersize
    t_l=np.average(pixels[0:c,0:c])
    b_l=np.average(pixels[601-c:601,0:c])
    b_r=np.average(pixels[601-c:601,601-c:601])
    t_r=np.average(pixels[0:c,601-c:601])


    return np.array([t_l,t_r,b_r,b_l])

def sides_av(filename,sidesize):
 
        pixels=read_in_img(filename)
        s=sidesize
 
        hs=np.int(s/2)
        top_side=np.average(pixels[0:s,300-hs:300+hs])
        bottom_side=np.average(pixels[601-s:601,300-hs:300+hs])
        right_side=np.average(pixels[300-hs:300+hs,601-s:601])
        left_side=np.average(pixels[300-hs:300+hs,0:s])

        return np.array([top_side,bottom_side,right_side,left_side])
    
    
   

def background_adjustment(filename,cornersize,sidesize):
    start=time.time()
    pixels=read_in_img(filename)
    sides=sides_av(filename,sidesize)
    corners=corners_av(filename,cornersize)
    highest_pixel=np.amax(np.ravel(pixels))
    print(sides)
    print(corners)
    
    for i in range(3):
        if sides[i] > 15:
            print('sides are not in background')
            sides[i]=0 
        if corners[i]>15:
            print('corners are not in background')
            corners[i]=0
    back_av=int(np.round(np.average(sides)/2+np.average(corners)/2))
                
    for i in range(3):
        
     
        if sides[i] == 0:
            sides[i]= back_av
        if corners[i] == 0:
            corners[i]= back_av
   
        
        
        
    print(back_av)
    print(sides)
    print(corners)
 

        
    pixels[0:201,0:201]-=int(np.round(corners[0])) #top left        
    pixels[201:401,0:201]-=int(np.round(sides[3])) #left
    pixels[401:601,0:201]-=int(np.round(corners[3])) #bottom left
    pixels[0:201,201:401]-=int(np.round(sides[0])) #top
    pixels[201:401,201:401]-=back_av #middle
    pixels[401:601,201:401]-=int(np.round(sides[1])) #bottom
    pixels[0:201,401:601]-=int(np.round(corners[1])) # top right
    pixels[201:401,401:601]-=int(np.round(sides[2])) # right
    pixels[401:601,401:601]-=int(np.round(corners[2])) #bottom right

     
       
   
       
    print(highest_pixel)
    a=np.where(pixels>highest_pixel)
    pixels[a]=0
     
       
    end=time.time()
    print(end-start)
    plt.figure(2)
    plt.imshow(pixels)
       
    plt.colorbar()
     
            
            

   
  
#%%
 

    
    
    
    
    
   




