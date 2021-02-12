# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 13:33:14 2021

@author: maxim
"""

"""
This works out a gradient)both x and y dirn) to find out background
Then finds fitness parameter for focal spot by squaring pixel values
and normalising to total pixel value.
"""

import numpy as np

import time

from skimage import io 

    
aperture_width=50 #in pixels
err=0

QP=0    

start=time.time()
def read_in_img(filename):
    pixel_values = 255*np.array(io.imread(filename, as_gray=True))
    y_max=len(pixel_values)#rows
    x_max=len(pixel_values[0])#columns
    pixel_values=np.delete(pixel_values,np.s_[y_max-20:y_max],0)
    return pixel_values


def centre_of_mass(IMG):
    sum_pix_val=np.sum(IMG)
    
    rows=len(IMG)
    cols=len(IMG[0])
    row_ind=np.arange(0,rows,1)#array of row indices
    
    col_ind=np.arange(0,cols,1)#array of column indices
    sum_rows=np.sum(IMG,axis=1)# array of sum of pixel values for each row
    sum_cols=np.sum(IMG,axis=0)# array of sum of pixel values for each column
    sum_wtd_rows=(sum_rows*row_ind)/sum_pix_val
    sum_wtd_cols=(sum_cols*col_ind)/sum_pix_val
    COM_row=np.sum(sum_wtd_rows)#COM row indices
    COM_col=np.sum(sum_wtd_cols)#COM column indices
    return round(COM_row), round(COM_col),sum_pix_val

def aperture(IMG):
    COM_row,COM_col,sum_pix_val=centre_of_mass(IMG)
    start_row=np.int(COM_row-(aperture_width/2))
    start_col=np.int(COM_col-(aperture_width/2))
    sum_aperture=0
    for v in range(start_row,start_row+aperture_width):
        sum_aperture+=np.sum(IMG[v,start_col:start_col+aperture_width])
    quality_p=sum_aperture/(sum_pix_val)
    global QP
    QP=quality_p
    return quality_p

def corners_av(pixels,cornersize):
    y_max=len(pixels)#rows
    x_max=len(pixels[0])#columns
    c=cornersize
    t_l=np.average(pixels[0:c,0:c])
    b_l=np.average(pixels[y_max-c:y_max,0:c])
    b_r=np.average(pixels[y_max-c:y_max,x_max-c:x_max])
    t_r=np.average(pixels[0:c,x_max-c:x_max])
    return np.array([t_l,t_r,b_r,b_l]) 

def grad(corners,pixels):
    y_max=len(pixels)#rows
    x_max=len(pixels[0])#columns
    Upper_grad=(corners[1]-corners[0])/x_max
    left_grad=(corners[3]-corners[0])/x_max
    bottom_grad=(corners[1]-corners[2])/y_max
    right_grad=(corners[3]-corners[2])/y_max
    return np.array([Upper_grad,left_grad,bottom_grad,right_grad])


def read(filename,cornersize):
    
    
    pixels=read_in_img(filename)
    total_pixels=np.sum(pixels)
    if total_pixels < 500000:
        return None 
    else:
        y_max=len(pixels)#rows
        x_max=len(pixels[0])#columns
 #   '''
#    This is needed as imread will not do maths properly on any pixel 
#    image reading will now output focal spot with background corrected
#    and a metric that correlates to shape of focal spot only
#    '''
        pixel_true=np.zeros((len(pixels),len(pixels[0])))#NEEDED AS THIS WILL NOT BE ABLE TO HANDLE MATHS OTHERWISE
        pixel_true[0:len(pixels),0:len(pixels[0])]=pixels[0:len(pixels),0:len(pixels[0])] #NEEDED 
    

    
        corners=corners_av(pixels,cornersize)
        grads=grad(corners,pixels)
    
   
        pixels_coord=np.mgrid[0:y_max,0:x_max].reshape(2,-1).T
    
   
        pixels_coord=(pixels_coord[0:len(pixels_coord),0]*grads[0]+pixels_coord[0:len(pixels_coord),1]*grads[1])+corners[0]
        pixel_background=pixels_coord.reshape(y_max,x_max)
        pixel_true=np.round(pixel_true-pixel_background)
   

   
        
        quality_param=aperture(pixel_true)

        fitness_param=np.sum(pixel_true**2)/(total_pixels)
        return fitness_param,pixel_true,total_pixels




