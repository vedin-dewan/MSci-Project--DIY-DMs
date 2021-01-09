# -*- coding: utf-8 -*-
"""
Read in and Analyse Focal Spot Images
"""
#Center of Mass Method to analyse Focal Spot

import numpy as np
from matplotlib import image
import time
import matplotlib.pyplot as plt
# from scipy.optimize import curve_fit
start=time.time()

Image_1="/Users/vedindewan/Desktop/MSci Project (AO)/Focal_Spot_Analysis/Test_Spot_Data/107_935_1798_1076_0.jpg"
Image_2="/Users/vedindewan/Desktop/MSci Project (AO)/Focal_Spot_Analysis/Test_Spot_Data/1163_1300_2061_703_1901.jpg"
Image_3="/Users/vedindewan/Desktop/MSci Project (AO)/Focal_Spot_Analysis/Test_Spot_Data/1168_1630_1922_640_1493.jpg"
Image_4="/Users/vedindewan/Desktop/MSci Project (AO)/Focal_Spot_Analysis/Test_Spot_Data/1178_2192_2173_666_277.jpg"

images=[Image_1,Image_2,Image_3,Image_4]
titles=["Focal_spot_1","Focal_spot_2","Focal_spot_3","Focal_spot_4"]

aperture_width=100 #in pixels
err=0
quality_param=np.zeros(len(images))
QP=0

def read_in_img(filename):
    pixel_values = np.array(image.imread(filename))
    return pixel_values


def center_of_mass(IMG):
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


def aperture(IMG,COM_row,COM_col,sum_pix_val):
    start_row=np.int(COM_row-(aperture_width/2))
    start_col=np.int(COM_col-(aperture_width/2))
    sum_aperture=0
    for v in range(start_row,start_row+aperture_width):
        sum_aperture+=np.sum(IMG[v,start_col:start_col+aperture_width])
    quality_p=sum_aperture/sum_pix_val
    global QP
    QP=quality_p
    return quality_p 

def plot(IMG,COM_row,COM_col,quality_parameter):
    plt.figure(i+1)
    plt.title(titles[i]+f" ,Quality_Pram-{QP}")
    plt.imshow(IMG)
    plt.colorbar()
    plt.scatter(COM_col,COM_row,marker='+',label='Centre of Mass')# row is y coordinate and column is x coordinate
    plt.legend()
    plt.show()
    return

def main(file,err,quality_param):
    Img=read_in_img(file)
    max_val=np.max(Img)
    if max_val>=255:#
        err+=1
        return
    COM_row,COM_col,sum_pix_val=center_of_mass(Img)
    quality_parameter= aperture(Img,COM_row,COM_col,sum_pix_val)
    quality_param[i]=quality_parameter
   
    return Img,COM_row,COM_col,quality_parameter

for i in range(4):
    Img,COM_row,COM_col,quality_parameter=main(images[i],err,quality_param)
    # print(QP)
    # plot(Img,COM_row,COM_col,QP)
    

end=time.time()
print((end-start))
print("quality_param=",quality_param)
        
#%% Pixel Value Squared Method to Analyse Focal Spot
start=time.time()
def read_in_img(filename):
    pixel_values = np.array(image.imread(filename))
    pixel_square=np.sum((pixel_values/254)**2)
    return pixel_values,pixel_square

for i in range(4):
    pixel_value,pixel_square=read_in_img(images[i])
    # print(pixel_square)

end=time.time()
print((end-start))







 
