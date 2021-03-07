# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 16:30:04 2021

@author: maxim
"""

from matplotlib import image
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from mpl_toolkits import mplot3d


def read_xyz_0(filename):
    dr= pd.read_csv(filename, delimiter='\t',skiprows=13,encoding= 'unicode_escape')
#   for 5 element    dr= pd.read_csv(filename, delimiter='\t',skiprows=13,encoding= 'unicode_escape')
    dr.columns=['Coordinates']#naming colums
    pd_df = dr.Coordinates.str.split(' ',expand=True)
    pd_df=pd_df.iloc[:-1,:3]#selecting first 3 colums
    pd_df = pd_df.apply (pd.to_numeric, errors='coerce')
    pd_df = pd_df.dropna()#removing colums with NaN values
    pd_df = pd_df.reset_index(drop=True)
    x_point=np.array(pd_df.iloc[:,0]).astype(np.float)#x position on grid (just numbers denoting position in grid)
    y_point=np.array(pd_df.iloc[:,1]).astype(np.float) #y position on grid (just numbers denoting position in grid)
    z_point_1=np.array(pd_df.iloc[:,2]).astype(np.float) # z position/height of a point on the grid (micro meters)
    x_point=x_point-np.min(x_point)#just resets grid to 0
    y_point=y_point-np.min(y_point)#just resets grid to zero
    
    X = x_point
    Y = y_point
    Z = z_point_1
    # plt.figure(fig_number)   #plots it before the tilt
    # plt.plot(Y,Z)
    """ Correct for tilt along x-axis"""
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
    """ Correct for tilt along y-axis"""
    
    X_1=[]
    Z_3=[]
    X_2=[]
    Z_4=[]
    for i in range(len(Y)):
        if Y[i]<100:
            X_1.append(Y[i])
            Z_3.append(Z[i])
        
        if Y[i]>500:
            X_2.append(Y[i])
            Z_4.append(Z[i])
    peak_3_index=Z_3.index(np.max(Z_3))
    peak_4_index=Z_4.index(np.max(Z_4))
    grad_1=(Z_4[peak_2_index]-Z_3[peak_3_index])/(X_2[peak_4_index]-X_1[peak_3_index])

     
    
    theta_1=-np.arctan(grad_1)
    
   
    return theta,theta_1


def create_circular_mask(h, w, center, radius):

    if center == None: # use the middle of the image
        center = (int(w/2), int(h/2))
    if radius == None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
   
    return mask,center

def hard_aperture(z_2d,radius):
    mask,center=create_circular_mask(len(z_2d),len(z_2d[0]),None,radius)
    #print(mask)
    for i in range(len(z_2d)):
        for j in range(len(z_2d[0])):
            if mask[i][j] == False:
               z_2d[i][j] = 0
    return z_2d

def read_xyz(filename,theta,theta_1):
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
    x_point=x_point-np.min(x_point)#just resets grid to 0
    y_point=y_point-np.min(y_point)#just resets grid to zero
    
    X = x_point
    Y = y_point
    Z = z_point_1
    # plt.figure(fig_number)   #plots it before the tilt
    # plt.plot(Y,Z)
   

     
    
    """Correct for tilt along x-axis"""
    X = x_point
    Y = y_point*np.cos(theta) - z_point_1*np.sin(theta)
    Z = y_point*np.sin(theta) + z_point_1*np.cos(theta)
    # plt.figure(fig_number+5)  # to check for the tilt
    # plt.plot(Y,Z)
    """ Correct for tilt along y-axis"""
    
    Y = Y
    X = X*np.cos(theta_1) - Z*np.sin(theta_1)
    Z = X*np.sin(theta_1) + Z*np.cos(theta_1)
    
    combined = np.vstack((X,Y,Z)).T

    
    x_range=int(np.round(np.max(X)-np.min(X)))
    y_range=int(np.round(np.max(Y)-np.min(Y)))
   

    z_2d=np.zeros((y_range+1,x_range+1))
    for i in range(len(combined)):
        y=int(np.round(combined[i,1]))
        x=int(np.round(combined[i,0]))
      
        z_2d[y,x]=combined[i,2]
    z_2d=hard_aperture(z_2d,250) 
    # plt.figure(fig_number)
    # plt.imshow(z_2d)
    # # plt.pcolor(v, r, z, )
    # plt.colorbar()
    # plt.show()
    
   
    return z_2d,Z,Y,X


def main(Image):
    Image_0=Image
    theta,theta_1=read_xyz_0(Image_0)
    z_2d,Z,Y,X=read_xyz(Image,theta,theta_1)
    #print(z_2d)
    # z_max=np.max(z_2d)
    return z_2d

# image_1=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\3_Element_DM_XYZ_Data\3_Element_DM_Test_21_11_2020_2H.xyz'
# z=main(image_1)

# plt.figure(10)

# plt.imshow(z)

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
    

