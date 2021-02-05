#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 02:43:03 2021

@author: vedindewan

2D FFT OF FOCALSPOT TO RETRIEVE PHASE
"""
import numpy as np
from matplotlib import image
import time
import matplotlib.pyplot as plt
from scipy import fftpack, ndimage

#Image="/Users/vedindewan/Desktop/MSci_Project_AO/Focal_Spot_Analysis/Test_Spot_Data/1163_1300_2061_703_1901.jpg"
Image="/Users/vedindewan/Desktop/MSci_Project_AO/Focal_Spot_Analysis/Test_Spot_Data/0_0.jpg"
Image="/Users/vedindewan/Desktop/MSci_Project_AO/FFT_focal_spot/2020-12-14_0112 (1).jpg"
def read_in_img(filename):
    pixel_values = np.array(image.imread(filename,'O'))
    # pixel_values=image.im2gray(pixel_values)
    return pixel_values
from skimage import io
pixels= io.imread(Image, as_gray=True)
# cut_img=np.zeros((200,200))
# pixels=read_in_img(Image)
# cut_img[0:200, 0:200]=pixels[200:400, 200:400]
print(pixels)
plt.figure(1)
plt.imshow(pixels)
plt.colorbar()
# phase=np.fft.fft2(pixels)
phase = np.fft.fftshift(np.abs(np.fft.fft2(pixels))) / np.sqrt(len(pixels))

plt.figure(2)
plt.imshow(np.log10(abs(phase)),vmin=None, vmax=None)
plt.colorbar()
print(phase)

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


#%%Read in xyx file

file="/Users/vedindewan/Desktop/MSci_Project_AO/Zygo _nterferometer/5_Element_DM_XYZ_Data/5_Element_DM_Test_21_11_2020_24D.xyz"
def read_xyz(filename):
    dr= pd.read_csv(filename, delimiter='\t',skiprows=13,encoding= 'unicode_escape')
    dr.columns=['Coordinates']#naming colums
    pd_df = dr.Coordinates.str.split(' ',expand=True)
    pd_df=pd_df.iloc[:-1,:3]#selecting first 3 colums
    pd_df = pd_df.apply (pd.to_numeric, errors='coerce')
    pd_df = pd_df.dropna()#removing colums with NaN values
    pd_df = pd_df.reset_index(drop=True)
    
   
    return pd_df
pd_df=read_xyz(file)


#%%
# Original Location of points
print(pd_df)
x_point=np.array(pd_df.iloc[:,0]).astype(np.float)#x position on grid (just numbers denoting position in grid)
y_point=np.array(pd_df.iloc[:,1]).astype(np.float) #y position on grid (just numbers denoting position in grid)
z_point_1=np.array(pd_df.iloc[:,2]).astype(np.float) # z position/height of a point on the grid (micro meters)
x_point=x_point-np.min(x_point)
y_point=y_point-np.min(y_point)
#rotate points
theta=0.0015
X = x_point
Y = y_point*np.cos(theta) - z_point_1*np.sin(theta)
Z = y_point*np.sin(theta) + z_point_1*np.cos(theta)

combined = np.vstack((X,Y,Z)).T
print(len(combined))

x_range=int(np.round(np.max(X)-np.min(X)))
y_range=int(np.round(np.max(Y)-np.min(Y)))
print(x_range,y_range)

z_2d=np.zeros((y_range+1,x_range+1))
for i in range(len(combined)):
    y=int(np.round(combined[i,1]))
    x=int(np.round(combined[i,0]))
    print(i)
    z_2d[y,x]=combined[i,2]
print(z_2d)
#%%

plt.imshow(z_2d)
plt.colorbar()

phase = np.fft.fftshift(np.abs(np.fft.fft2(z_2d))) / np.sqrt(len(z_2d))

plt.figure(2)
plt.imshow(np.log10(abs(phase)),vmin=None, vmax=None)
plt.colorbar()
















