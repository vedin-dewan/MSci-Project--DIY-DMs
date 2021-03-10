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
from skimage.transform import resize
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
    # plt.figure(1)   #plots it before the tilt
    # plt.title('Z displacment vs Y axis before tilt')
    # plt.plot(Y,Z)
    # plt.show()
    # plt.figure(2)
    # plt.title('Z displacement vs X axis before tilt')
    # plt.plot(X,Z)
    # plt.show()
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
    # plt.figure(3)  # to check for the tilt
    # plt.plot(Y,Z)
    """ Correct for tilt along y-axis"""
    
    X_1=[]
    Z_3=[]
    X_2=[]
    Z_4=[]
    for i in range(len(X)):
        if X[i]<100:
            X_1.append(X[i])
            Z_3.append(Z[i])
        
        if X[i]>500:
            X_2.append(X[i])
            Z_4.append(Z[i])
    peak_3_index=Z_3.index(np.max(Z_3))
    peak_4_index=Z_4.index(np.max(Z_4))
    grad_1=(Z_4[peak_4_index]-Z_3[peak_3_index])/(X_2[peak_4_index]-X_1[peak_3_index])

     
    
    theta_1=-np.arctan(grad_1)
    
   
    return theta,theta_1


def resize_image(z_2D,height,width):
    resized=resize(z_2D,(height,width))
    return resized

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
    
    # X = x_point
    # Y = y_point
    # Z = z_point_1
    # plt.figure(3)   #plots it before the tilt
    # plt.title('Z displacement vs Y values repeated')
    # plt.plot(Y,Z)
   

     
    
    """Correct for tilt along x-axis"""
    X = x_point
    Y = y_point*np.cos(theta) - z_point_1*np.sin(theta)
    Z = y_point*np.sin(theta) + z_point_1*np.cos(theta)

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
    # z_2d=hard_aperture(z_2d,250) 
    # plt.figure(fig_number)
    # plt.imshow(z_2d)
    # plt.pcolor(v, r, z, )
    # plt.colorbar()
    # plt.show()
    # plt.figure(3)  # to check for the tilt
    # plt.title('Check for tilt for Y')
    # plt.plot(Y,Z)
    # plt.show()
    
    # plt.figure(4)# to check for the tilt
    # plt.title('Check for tilt for X')
    # plt.plot(X,Z)
    # plt.show()
    combined = np.vstack((X,Y,Z)).T
   
    return z_2d,Z,Y,X


# def main(Image,actuators_on=None):
   
#     Image_0=Image
#     theta_y,theta_x=read_xyz_0(Image_0)
#     if actuators_on == 2 :
#         z_2d,Z,Y,X=read_xyz(Image,theta_y,0)
#         return z_2d
#     if actuators_on == 4 :
#         z_2d,Z,Y,X=read_xyz(Image,theta_y,0)
#         return z_2d
    
#     if actuators_on == 1 :
#         z_2d,Z,Y,X=read_xyz(Image,0,theta_x)
#         return z_2d
#     if actuators_on == 5 :
#         z_2d,Z,Y,X=read_xyz(Image,0,theta_x)
#         return z_2d
#     else:
    
#         z_2d,Z,Y,X=read_xyz(Image,theta_y,theta_x)
#         return z_2d
def main(Image,actuators_on=None):
   
    Image_0=Image
    theta_y,theta_x=read_xyz_0(Image_0)
    if actuators_on == 2 :
        z_2d,Z,Y,X=read_xyz(Image,theta_y,0)
        Z_2d=resize_image(z_2d,600,600)
        Z_offset=hard_aperture(Z_2d,250)
        Z_2d=Z_2d-np.min(Z_offset[Z_offset>0])
        Z_2D=hard_aperture(Z_2d,250)
        return Z_2D
    if actuators_on == 4 :
        z_2d,Z,Y,X=read_xyz(Image,theta_y,0)
        Z_2d=resize_image(z_2d,600,600)
        Z_offset=hard_aperture(Z_2d,250)
        Z_2d=Z_2d-np.min(Z_offset[Z_offset>0])
        Z_2D=hard_aperture(Z_2d,250)
        return Z_2D
    
    if actuators_on == 1 :
        z_2d,Z,Y,X=read_xyz(Image,0,theta_x)
        Z_2d=resize_image(z_2d,600,600)
        Z_offset=hard_aperture(Z_2d,250)
        Z_2d=Z_2d-np.min(Z_offset[Z_offset>0])
        Z_2D=hard_aperture(Z_2d,250)
        return Z_2D
    if actuators_on == 5 :
        Z_2D,Z,Y,X=read_xyz(Image,0,theta_x)
        Z_2d=resize_image(z_2d,600,600)
        Z_offset=hard_aperture(Z_2d,250)
        Z_2d=Z_2d-np.min(Z_offset[Z_offset>0])
        Z_2D=hard_aperture(Z_2d,250)

        return Z_2D
    else:
    
        z_2d,Z,Y,X=read_xyz(Image,theta_y,theta_x)
        Z_2d=resize_image(z_2d,600,600)
        Z_offset=hard_aperture(Z_2d,250)

        Z_2d=Z_2d-np.min(Z_offset[Z_offset>0])
        
        Z_2D=hard_aperture(Z_2d,250)
        return Z_2D
    
    


    #print(z_2d)
    # z_max=np.max(z_2d)

# image_0=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_00.xyz'
# image_1=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_00.xyz'
# z=main(image_1,0)

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
    

