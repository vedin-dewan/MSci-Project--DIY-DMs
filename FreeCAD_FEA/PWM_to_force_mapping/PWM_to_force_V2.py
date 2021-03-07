# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 11:09:14 2021

@author: maxim
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import zernike_polynomials as zp
import scipy.optimize as opt
import reading_xyz_data_tilt_v2 as read_xyz

def read_FEM(file):
    pd_df = pd.read_csv(file,header=None,encoding ='utf-8' ,dtype='a')
#Original Location of points
    z_point=pd_df.iloc[1:,17].tolist()
    z_point=[float(i) for i in z_point]

    x_point=pd_df.iloc[1:,15].tolist()
    x_point=[float(i) for i in x_point]

    y_point=pd_df.iloc[1:,16].tolist()
    y_point=[float(i) for i in y_point]

#displacement of points in the z-direction/normal to mirror surface
    z_disp=pd_df.iloc[1:,2].tolist()
    z_disp=[float(i) for i in z_disp]

# Finding points just on the surface of the mirror and their displacement (i.e where z_point=0)
    indices=np.where(np.isclose(z_point, 0.000, 0.000001))#last argument is the tolerence
    # indices=np.where(z_point ==0)
    indices=indices[0]#quirk of np.where

    x_point_surf=np.take(x_point,indices)
    y_point_surf=np.take(y_point,indices)
    z_disp=np.take(z_disp,indices)
    
    X=x_point_surf
    Y=y_point_surf
    Z=z_disp
    
    combined = np.vstack((X,Y,Z)).T
    
    x_range=int(np.round(np.max(X)-np.min(X)))
    y_range=int(np.round(np.max(Y)-np.min(Y)))
   

    z_2d=np.zeros((x_range+1,y_range+1))
    for i in range(len(combined)):
        y=int(np.round(combined[i,1])+25)
        x=int(np.round(combined[i,0])+25)
      
        z_2d[y,x]=combined[i,2]
    # plt.figure(1)
    # plt.imshow(z_2d)

    return z_2d

# def centre_of_mass(z_2d):
#     sum_pix_val=np.sum(z_2d)
    
#     rows=len(z_2d)
#     cols=len(z_2d[0])
#     row_ind=np.arange(0,rows,1)#array of row indices
    
#     col_ind=np.arange(0,cols,1)#array of column indices
#     sum_rows=np.sum(z_2d,axis=1)# array of sum of pixel values for each row
#     sum_cols=np.sum(z_2d,axis=0)# array of sum of pixel values for each column
#     sum_wtd_rows=(sum_rows*row_ind)/sum_pix_val
#     sum_wtd_cols=(sum_cols*col_ind)/sum_pix_val
#     COM_row=np.sum(sum_wtd_rows)#COM row indices
#     COM_col=np.sum(sum_wtd_cols)#COM column indices
#     row=int(round(COM_row))
#     col=int(round(COM_col))
#     return row,col
    


def PWM_to_force(FEM,interferogram_files,PWM_values,force_values,fig_number):#has to be an array of all equal lengths
 
    #FEM=FEM_files
    INTER=interferogram_files
    PWM=PWM_values
    forces=force_values
    
    # if len(PWM_values) !=len(INTER):
    #     print('Length of PWM values and interferogram files not the same')

    # if len(FEM) != len(forces_values):
    #     print('length of FEM files and force values not the same')

    
    displacements_inter=[]
    z_2d=INTER
    for i in range(len(INTER)):
        z_min=np.min(z_2d[i][z_2d[i]>0])
        z_max=np.max(z_2d[i])
        #print(z_max)
        displacements_inter.append(z_max-z_min)
    
        
    #print(displacements_inter)

    
    displacements_FEM=[]
    #print(displacements_inter)

    
    for i in range(len(FEM)):
        #print(read_FEM(FEM[i]))
        displacements_FEM.append(1000*np.max(read_FEM(FEM[i])))
    
    #print(displacements_FEM)
    grad_PWM_INTER=np.polyfit(PWM,displacements_inter,1)
    grad_forces_FEM=np.polyfit(forces,displacements_FEM,1)
    #print(grad_forces_FEM)
    
    PWM_graph=np.linspace(0,4095,4095)
    
    grad_PWM_force=grad_PWM_INTER[0]/grad_forces_FEM[0]
    intercept=(grad_PWM_INTER[1]-grad_forces_FEM[1])/grad_forces_FEM[0]
    forces_PWM=grad_PWM_force*PWM_graph+intercept
    
    plt.figure(fig_number)
    plt.title('PWM values vs maximum displacement')
    plt.errorbar(PWM,displacements_inter,fmt='o')
    plt.plot(PWM_graph,grad_PWM_INTER[0]*PWM_graph+grad_PWM_INTER[1])
    
    plt.figure(fig_number+1)
    plt.title('PWM values vs Force')
    plt.plot(PWM_graph,forces_PWM)
    
    return grad_PWM_force,intercept

def PWM_force_output(grad_PWM_force,intercept,PWM):
    force=grad_PWM_force*PWM+intercept
    print(force)
    return force

def PWM_to_force_av(FEM,interferogram_files,PWM_values,force_values,fig_number):#has to be an array of all equal lengths
 
    #FEM=FEM_files
    INTER=interferogram_files
    PWM=PWM_values
    forces=force_values
    
    # if len(PWM_values) !=len(INTER):
    #     print('Length of PWM values and interferogram files not the same')

    # if len(FEM) != len(forces_values):
    #     print('length of FEM files and force values not the same')

    
    #displacements_inter=[]
    z_2d=INTER
    # for i in range(len(INTER)):
    #     z_min=np.min(z_2d[i][z_2d[i]>0])
    #     z_max=np.max(z_2d[i])
    #     #print(z_max)
    #     displacements_inter.append(z_max-z_min)
    
        
    #print(displacements_inter)

    
    displacements_FEM=[]
    #print(displacements_inter)

    
    for i in range(len(FEM)):
        #print(read_FEM(FEM[i]))
        displacements_FEM.append(1000*np.max(read_FEM(FEM[i])))
    
    #print(displacements_FEM)
    grad_PWM_INTER=np.polyfit(PWM,z_2d,1)
    grad_forces_FEM=np.polyfit(forces,displacements_FEM,1)
    #print(grad_forces_FEM)
    
    PWM_graph=np.linspace(0,4095,4095)
    
    grad_PWM_force=grad_PWM_INTER[0]/grad_forces_FEM[0]
    intercept=(grad_PWM_INTER[1]-grad_forces_FEM[1])/grad_forces_FEM[0]
    forces_PWM=grad_PWM_force*PWM_graph+intercept
    
    plt.figure(fig_number)
    plt.title('PWM values vs maximum displacement')
    plt.errorbar(PWM,z_2d,fmt='o')
    plt.plot(PWM_graph,grad_PWM_INTER[0]*PWM_graph+grad_PWM_INTER[1])
    
    plt.figure(fig_number+1)
    plt.title('PWM values vs Force')
    plt.plot(PWM_graph,forces_PWM)
    
    return grad_PWM_force,intercept

