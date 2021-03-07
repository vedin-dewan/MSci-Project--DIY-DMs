# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 18:35:33 2021

@author: maxim
"""

import numpy as np 
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt


def Z0_0(x,y):
    return 1
def Zneg1_1(x,y,radius,phase,amp):
    Z=np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            r=np.sqrt(x[i]**2+y[j]**2)
            if r >=radius:
                Z[i][j] +=0
            else:            
                phi=np.arctan2(y[j],x[i])                              
                z=amp*2*r*np.sin(phi+phase)
                Z[i][j]+=z
    return Z 
    

def Z1_1(x,y,radius,phase,amp):
    #print(len(x),len(y))
    Z=np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            r=np.sqrt(x[i]**2+y[j]**2)
            if r>radius:
                Z[i][j] +=0
            else:
                phi=np.arctan2(y[j],x[i])
                z=amp*2*r*np.cos(phi+phase)
                Z[i][j] +=z
    return Z
   
def Zneg2_2(x,y,radius,phase,amp):
    Z=np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            r=np.sqrt(x[i]**2+y[j]**2)
            if r>radius:
                Z[i][j] +=0
            else:
                phi=np.arctan2(y[j],x[i])
                z=amp*np.sqrt(6)*(r**2)*np.sin(2*phi)
                Z[i][j] +=z
    return Z

def Z0_2(x,y,radius,phase,amp):
    Z=np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            r=np.sqrt(x[i]**2+y[j]**2)
            if r>radius:
                Z[i][j] +=0
            else:
                z=amp*np.sqrt(3)*(2*(r**2)-1)
                Z[i][j] +=z
    return Z

def Z2_2(x,y,radius,phase,amp):
    Z=np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            r=np.sqrt(x[i]**2+y[j]**2)
            if r >= radius: 
                Z[i][j]+=0
            else:
                phi=np.arctan2(y[j],x[i])
                z=amp*np.sqrt(6)*(r**2)*np.cos(2*phi)
                Z[i][j] += z
    return Z


def Zneg3_3(x,y,radius,phase,amp):
    Z=np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):            
            r=np.sqrt(x[i]**2+y[j]**2)
            if r >radius:
                Z[i][j]+=0
            else:
                phi=np.arctan2(y[j],x[i])
                z=amp*np.sqrt(8)*(r**3)*np.sin(3*phi)
                Z[i][j] +=z
    return Z

    
def Zneg1_3(x,y,radius,phase,amp):
    Z=np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
             r=np.sqrt(x[i]**2+y[j]**2)
             if r>radius:
                 Z[i][j]+=0
             else:
                phi=np.arctan2(y[j],x[i])
                z=amp*np.sqrt(8)*(3*r**3-2*r)*np.sin(phi)
                Z[i][j]+=z
    return Z

def Z1_3(x,y,radius,phase,amp):
    Z=np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
             r=np.sqrt(x[i]**2+y[j]**2)
             if r>radius:
                 Z[i][j]+=0
             else:
                 phi=np.arctan2(y[j],x[i])
                 z=amp*np.sqrt(8)*(3*r**3-2*r)*np.cos(phi)
                 Z[i][j]+=z
    return Z

    
def Z3_3(x,y,radius,phase,amp):
    Z=np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
             r=np.sqrt(x[i]**2+y[j]**2)
             if r >radius:
                 Z[i][j]+=0
             else:
                phi=np.arctan2(y[j],x[i])
                z=amp*np.sqrt(8)*(r**3)*np.cos(3*phi)
                Z[i][j]+=z
    return Z



def Zneg4_4(x,y,radius,phase,amp):
    Z=np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            r=np.sqrt(x[i]**2+y[j]**2)
            if r >radius:
                Z[i][j]+=0
            else:
                phi=np.arctan2(y[j],x[i])
                z=amp*np.sqrt(10)*(r**4)*np.sin(4*phi)
                Z[i][j]+=z
    return Z
 

def Zneg2_4(x,y,radius,phase,amp):
    Z=np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            r=np.sqrt(x[i]**2+y[j]**2)            
            if r>radius:
                Z[i][j]+=0
            else:
                phi=np.arctan2(y[j],x[i])
                z=amp*np.sqrt(10)*(4*r**4-3*r**2)*np.sin(2*phi)
                Z[i][j]+=z
    return Z


def Z0_4(x,y,radius,phase,amp):
    Z=np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            r=np.sqrt(x[i]**2+y[j]**2)
            if r>radius:
                Z[i][j]+=0
            else:
                z=amp*np.sqrt(5)*(6*r**4-6*r**2+1)
                Z[i][j]+=z
    return Z


def Z2_4(x,y,radius,phase,amp):
    Z=np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            r=np.sqrt(x[i]**2+y[j]**2)
            if r>radius:
                Z[i][j]+=0
            else:
                phi=np.arctan2(y[j],x[i])
                z=amp*np.sqrt(10)*(4*r**4-3*r**2)*np.cos(2*phi)
                Z[i][j]+=z
    return Z


def Z4_4(x,y,radius,phase,amp):
    Z=np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            r=np.sqrt(x[i]**2+y[j]**2)
            if r>radius:
                Z[i][j]+=0
            else:
                phi=np.arctan2(y[j],x[i])
                z=amp*np.sqrt(10)*(r**4)*np.cos(4*phi)
                Z[i][j]+=z
    return Z

    
def delta(x):
    if x == 0:
        return 1
    else:
        return 0

def gauss(x,y,w,P,radius,sigma):
    Z=np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            r=np.sqrt(x[i]**2+y[j]**2)
            if r>radius:
                Z[i][j]+=0
            else:          
                z=(P/(np.pi*w**2))*np.exp((-(r/w)**2)*sigma)
                Z[i][j] +=z
    return Z

def shah_gauss(x,y,positions,radius):
    Z=np.zeros((len(x),len(y)))
    for p in range(len(positions)):
        for i in range(-150,151):
            for j in range(-150,151):
                centre_x=positions[p][0]
                centre_y=positions[p][1]
                x_index=positions[p][0]+i
                y_index=positions[p][1]+j
                x_gauss=np.exp(-((x[x_index]-x[centre_x])**2)*15)
                y_gauss=np.exp(-((y[y_index]-y[centre_y])**2)*15)
                z=1*x_gauss*y_gauss
                Z[x_index][y_index]+=z
    return Z
def shah(x,y,positions,radius):
    Z=np.zeros((len(x),len(y)))
    for p in range(len(positions)):
        for i in range(-50,51):
            for j in range(-50,51):
                centre_x=positions[p][0]
                centre_y=positions[p][1]
                x_index=positions[p][0]+i
                y_index=positions[p][1]+j
                x_shah=delta(x[x_index]-x[centre_x])
                y_shah=delta(y[y_index]-y[centre_y])
                z=x_shah*y_shah
                Z[x_index][y_index]+=z
    return Z
def fourier(coordinates_with_values,fig):
    pixels=coordinates_with_values
    phase = np.fft.fftshift(np.abs(np.fft.fft2(pixels))) / np.sqrt(len(pixels))
    if fig == 0:
        return phase
    else:
        plt.figure(fig)
        plt.imshow(np.log10(abs(phase)),vmin=None, vmax=None)
        plt.colorbar()
        return phase
def inverse_fourier(coordinates_with_values,fig):
    pixels=coordinates_with_values
    phase = np.fft.ifftshift(np.abs(np.fft.ifft2(pixels))) / np.sqrt(len(pixels))
    if fig == 0:
        return phase
    else:
        plt.figure(fig)
        plt.imshow(np.log10(abs(phase)),vmin=None, vmax=None)
        plt.colorbar()
    return phase




x=np.linspace(-1,1,601)
y=np.linspace(-1,1,601)

positions=([600,600],[0,600],[0,1],[600,599])


# surface=shah(x,y,positions)
# print(surface)
# print(surface)
# # print(surface[300])
# plt.imshow(surface)

    


