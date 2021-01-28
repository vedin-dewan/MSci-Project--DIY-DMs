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

def corners(filename,cornersize):
    if cornersize == 0:
        return None
    if cornersize > 0:
        
        pixels=read_in_img(filename)
        c=cornersize
        corner1=[]
        corner2=[]
        corner3=[]
        corner4=[]
        for i in range(0,c):
            for j in range(0,c):
                corner1.append(pixels[i][j])
        for i in range(0,c):
            for j in range(601-c,601):
                corner2.append(pixels[i][j])
        for i in range(601-c,601):
            for j in range(0,c):
                corner3.append(pixels[i][j])
        for i in range(601-c,601):
            for j in range(601-c,601):
                corner4.append(pixels[i][j])
        #corner_up_left=np.reshape(np.array(corner1),(c,c))
        #corner_up_right=np.reshape(np.array(corner2),(c,c))
        #corner_down_left=np.reshape(np.array(corner3),(c,c))
        #corner_down_right=np.reshape(np.array(corner4),(c,c))
        return np.array([corner1]),np.array([corner2]),np.array([corner3]),np.array([corner4])

def sides(filename,sidesize):
    if sidesize == 0:
        return None
    if sidesize > 0:
        pixels=read_in_img(filename)
        s=sidesize
        top_side=[]
        bottom_side=[]
        right_side=[]
        left_side=[]
        hs=np.int(s/2)
        for i in range(0,s):
            for j in range(300-hs,300+hs):
                top_side.append(pixels[i][j])
        for i in range(601-s,601):
            for j in range(300-hs,300+hs):
                bottom_side.append(pixels[i][j])
        for i in range(300-hs,300+hs):
            for j in range(601-s,601):
                right_side.append(pixels[i][j])
        for i in range(300-hs,300+hs):
            for j in range(0,s):
                left_side.append(pixels[i][j])
        #rightside=np.reshape(np.array(right_side),(s,s))
        #leftside=np.reshape(np.array(left_side),(s,s))
        #topside=np.reshape(np.array(top_side),(s,s))
        #bottomside=np.reshape(np.array(bottom_side),(s,s))
        return np.array([top_side]),np.array([bottom_side]),np.array([left_side]),np.array([right_side])
    
    
   
    
def b_a_corners(filename,squaresize):
    c_UL_val,c_UR_val,c_DL_val,c_DR_val=corners(filename,squaresize)
    c_UL_av=np.mean(c_UL_val)
    c_UR_av=np.mean(c_UR_val)
    c_DL_av=np.mean(c_DL_val)
    c_DR_av=np.mean(c_DR_val)
    
    return np.array([c_UL_av,c_UR_av,c_DL_av,c_DR_av])

def b_a_sides(filename,squaresize):
    top_val,bottom_val,left_val,right_val=sides(filename,squaresize)
    t_av=np.mean(top_val)
    b_av=np.mean(bottom_val)
    r_av=np.mean(left_val)
    l_av=np.mean(right_val)
    
    return np.array([t_av,b_av,r_av,l_av])

def background_adjustment(filename,cornersize,sidesize):
    start=time.time()
    pixels=read_in_img(filename)
    sides=b_a_sides(filename,sidesize)
    corners=b_a_corners(filename,cornersize)
    for i in range(3):
        if sides[i] > 20:
            print('sides are not in background')
            sides[i]=0 
    if sides.any() !=0 :
        middle=(np.average(sides)+np.average(corners))/2
        print(middle)
        for i in range(0,201):
            for j in range(0,201):
                if pixels[i,j]<corners[0]:
                    pixels[i,j]=0
                else:
                    pixels[i,j]=pixels[i,j]-corners[0]
        for i in range(201,401):
            for j in range(0,201):
                 if pixels[i,j]<sides[3]:
                    pixels[i,j]=0
                 else:
                    pixels[i,j]=pixels[i,j]-sides[3]
        for i in range(401,601):
            for j in range(0,201):
                if pixels[i,j]<corners[3]:
                    pixels[i,j]=0
                else:
                    pixels[i,j]=pixels[i,j]-corners[3]
                
        for i in range(0,201):
            for j in range(201,401):
                 if pixels[i,j]<sides[0]:
                    pixels[i,j]=0
                 else:
                    pixels[i,j]=pixels[i,j]-sides[0]
        for i in range(201,401):
            for j in range(201,401):
                 if pixels[i,j]<middle:
                    pixels[i,j]=0
                 else:
                    pixels[i,j]=pixels[i,j]-middle
        for i in range(401,601):
            for j in range(201,401):
                 if pixels[i,j]<sides[1]:
                    pixels[i,j]=0
                 else:
                    pixels[i,j]=pixels[i,j]-sides[1]
        for i in range(0,201):
            for j in range(401,601):
                 if pixels[i,j]<corners[1]:
                    pixels[i,j]=0
                 else:
                    pixels[i,j]=pixels[i,j]-corners[1]
                #print(pixels[i,j])
        for i in range(201,401):
            for j in range(401,601):
                 if pixels[i,j]<sides[2]:
                    pixels[i,j]=0
                 else:
                    pixels[i,j]=pixels[i,j]-sides[2]
        for i in range(401,601):
            for j in range(401,601):
                 if pixels[i,j]<corners[2]:
                    pixels[i,j]=0
                 else:
                    pixels[i,j]=pixels[i,j]-corners[2]
        end=time.time()
       
        print(end-start)
       
        
       
    
        #print(adjusted_pixels_raw)
       # adjusted_pixels=np.reshape(np.array(adjusted_pixels_raw),(601,601))
        #plt.figure(2)
        #plt.imshow(pixels)
        #plt.imshow(pixels)
        #plt.colorbar()
     
            
            
#test_c=b_a_corners('0_0.jpg',6) 
#print(test_c)
#test_s=b_a_sides('0_0.jpg',6)   
#print(test_s)
   
background_adjustment('0_0.jpg',6,6)   
#%%
 
def background_adjustment(filename,cornersize,sidesize):
    pixels=read_in_img(filename)
    sides=b_a_sides(filename,sidesize)
    corners=b_a_corners(filename,cornersize)
    print(corners)
    print(sides)
    adjusted_pixels_raw=[]
    for i in range(3):
        if sides[i] > 20:
            print('sides are not in background')
            sides[i]=0 
    if sides.any() !=0 :
        middle=(np.average(sides)+np.average(corners))/2
        for i in range(0,201):
            for j in range(0,201):
                adjusted_pixels_raw.append(pixels[i][j]-corners[0])
        for i in range(201,401):
            for j in range(0,201):
                adjusted_pixels_raw.append(pixels[i][j]-sides[0])
        for i in range(401,601):
            for j in range(0,201):
                adjusted_pixels_raw.append(pixels[i][j]-corners[1])
        for i in range(0,201):
            for j in range(201,401):
                adjusted_pixels_raw.append(pixels[i][j]-sides[3])
        for i in range(201,401):
            for j in range(201,401):
                adjusted_pixels_raw.append(pixels[i][j]-middle)
        for i in range(401,601):
            for j in range(201,401):
                adjusted_pixels_raw.append(pixels[i][j]-sides[2])
        for i in range(0,201):
            for j in range(401,601):
                adjusted_pixels_raw.append(pixels[i][j]-corners[2])
        for i in range(201,401):
            for j in range(401,601):
                adjusted_pixels_raw.append(pixels[i][j]-sides[1])
        for i in range(401,601):
            for j in range(401,601):
                adjusted_pixels_raw.append(pixels[i][j]-corners[3])
        #print(adjusted_pixels_raw)
        adjusted_pixels=np.reshape(np.array(adjusted_pixels_raw),(601,601))
        #plt.imshow(pixels)
        plt.imshow(adjusted_pixels)
        plt.colorbar()
    
    
    
    
    
    
   




