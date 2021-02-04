# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 16:15:04 2021

@author: maxim
"""
'''
This just averages the corners and subtracts them 
'''
#To measure corners of the focal spot

import numpy as np
from matplotlib import image
import time
import matplotlib.pyplot as plt

def read_in_img(filename):
    pixel_values = np.array(image.imread(filename))
    return pixel_values

def corners_av(filename,cornersize):
    pixels=read_in_img(filename)
    c=cornersize
    t_l=np.average(pixels[0:c,0:c])
    b_l=np.average(pixels[601-c:601,0:c])
    b_r=np.average(pixels[601-c:601,601-c:601])
    t_r=np.average(pixels[0:c,601-c:601])
    return np.array([t_l,t_r,b_r,b_l])

# def sides_av(filename,sidesize): 
#         pixels=read_in_img(filename)
#         s=sidesize 
#         hs=np.int(s/2)
#         top_side=np.average(pixels[0:s,300-hs:300+hs])
#         bottom_side=np.average(pixels[601-s:601,300-hs:300+hs])
#         right_side=np.average(pixels[300-hs:300+hs,601-s:601])
#         left_side=np.average(pixels[300-hs:300+hs,0:s])
#         return np.array([top_side,bottom_side,right_side,left_side])
       
def read(filename,cornersize):
    start=time.time()
    pixels=read_in_img(filename)
    corners=corners_av(filename,cornersize)
    highest_pixel=np.amax(np.ravel(pixels))

            
    pixels[0:301,0:301] -=int(np.round(corners[0]))
    pixels[301:601,0:301] -=int(np.round(corners[3]))
    pixels[0:301,301:601] -=int(np.round(corners[1]))
    pixels[301:601,301:601] -=int(np.round(corners[2]))
      
   
    # pixels[0:201,0:201]-=int(np.round(corners[0])) #top left        
    # pixels[201:401,0:201]-=int(np.round(sides[3])) #left
    # pixels[401:601,0:201]-=int(np.round(corners[3])) #bottom left
    # pixels[0:201,201:401]-=int(np.round(sides[0])) #top
    # pixels[201:401,201:401]-=back_av #middle
    # pixels[401:601,201:401]-=int(np.round(sides[1])) #bottom
    # pixels[0:201,401:601]-=int(np.round(corners[1])) # top right
    # pixels[201:401,401:601]-=int(np.round(sides[2])) # right
    # pixels[401:601,401:601]-=int(np.round(corners[2])) #bottom right
  
    a=np.where(pixels>highest_pixel)
    pixels[a]=0
    total_pixels=np.sum(pixels)
    '''
    This is needed as imread will not do maths properly on any pixel 
    image reading will now output focal spot with background corrected
    and a metric that correlates to shape of focal spot only
    '''
    pixel_true=np.zeros((len(pixels),len(pixels[0])))#NEEDED AS THIS WILL NOT BE ABLE TO HANDLE MATHS OTHERWISE
    pixel_true[0:len(pixels),0:len(pixels[0])]=pixels[0:len(pixels),0:len(pixels[0])] #NEEDED 
    fitness_parameter=np.sum(pixel_true**2)/(total_pixels)
    end=time.time()
    print(end-start)
    print(fitness_parameter)
    plt.imshow(pixel_true)
    return pixel_true,fitness_parameter


read('0_0.jpg',6)    

    
        
            
            

   

 

    
    
    
    
    
   




