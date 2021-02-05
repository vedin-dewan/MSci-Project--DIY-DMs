# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 13:05:38 2021

@author: maxim
"""


from matplotlib import image
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from mpl_toolkits import mplot3d



def read_xyz(filename,fig_number):
    dr= pd.read_csv(filename, delimiter='\t',skiprows=13,encoding= 'unicode_escape')
    dr.columns=['Coordinates']#naming colums
    pd_df = dr.Coordinates.str.split(' ',expand=True)
    pd_df=pd_df.iloc[:-1,:3]#selecting first 3 colums
    pd_df = pd_df.apply (pd.to_numeric, errors='coerce')
    pd_df = pd_df.dropna()#removing colums with NaN values
    pd_df = pd_df.reset_index(drop=True)
    x_point=np.array(pd_df.iloc[:,0]).astype(np.float)#x position on grid (just numbers denoting position in grid)
    y_point=np.array(pd_df.iloc[:,1]).astype(np.float) #y position on grid (just numbers denoting position in grid)
    z_point_1=np.array(pd_df.iloc[:,2]).astype(np.float) # z position/height of a point on the grid (micro meters)
    x_point=x_point-np.min(x_point)
    y_point=y_point-np.min(y_point)
    #rotate points
    theta=0
    X = x_point
    Y = y_point*np.cos(theta) - z_point_1*np.sin(theta)
    Z = y_point*np.sin(theta) + z_point_1*np.cos(theta)
    #plt.figure(fig_number)   #plots it before the tilt
   # plt.plot(Y,Z)
    Y_1=[]
    Z_1=[]
    Y_2=[]
    Z_2=[]
    for i in range(len(Y)):
        if Y[i]<100:
            Y_1.append(Y[i])
            Z_1.append(Z[i])
        
        if Y[i]>500:
            Y_2.append(Y[i])
            Z_2.append(Z[i])
    peak_1_index=Z_1.index(np.max(Z_1))
    peak_2_index=Z_2.index(np.max(Z_2))
    grad=(Z_2[peak_2_index]-Z_1[peak_1_index])/(Y_2[peak_2_index]-Y_1[peak_1_index])

     
    
    theta=-np.arctan(grad)
    X = x_point
    Y = y_point*np.cos(theta) - z_point_1*np.sin(theta)
    Z = y_point*np.sin(theta) + z_point_1*np.cos(theta)
    # plt.figure(fig_number+5)  # to check for the tilt
    # plt.plot(Y,Z)

    combined = np.vstack((X,Y,Z)).T

    
    x_range=int(np.round(np.max(X)-np.min(X)))
    y_range=int(np.round(np.max(Y)-np.min(Y)))
   

    z_2d=np.zeros((y_range+1,x_range+1))
    for i in range(len(combined)):
        y=int(np.round(combined[i,1]))
        x=int(np.round(combined[i,0]))
      
        z_2d[y,x]=combined[i,2]
    plt.figure(fig_number)
    plt.imshow(z_2d)
    plt.colorbar()

    
   
    return z_2d,Z,Y,X

#%%
'''
This part shows how the tilt is corrected for 
'''

def tilt_check_Z_Y(Z,Y,fig_number):
    plt.figure(fig_number)
    plt.plot(Y,Z,'o',color='red')
    Y_1=[]
    Z_1=[]
    Y_2=[]
    Z_2=[]
    for i in range(len(Y)):
        if Y[i]<100:
            Y_1.append(Y[i])
            Z_1.append(Z[i])
        
        if Y[i]>500:
            Y_2.append(Y[i])
            Z_2.append(Z[i])
    peak_1_index=Z_1.index(np.max(Z_1))
    peak_2_index=Z_2.index(np.max(Z_2))
    grad=(Z_2[peak_2_index]-Z_1[peak_1_index])/(Y_2[peak_2_index]-Y_1[peak_1_index])
    c=Z_2[peak_2_index]-grad*Y_2[peak_2_index]
    y=np.arange(600)
    z=grad*y+c
 
 

 
    
  
    plt.show()




