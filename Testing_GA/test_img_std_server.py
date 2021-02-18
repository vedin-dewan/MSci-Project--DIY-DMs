#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 13:07:52 2021
@author: maximillianstunt & vedindewan 
"""
"""
This takes data to measure the noise in the camera images for a constant
set of PWM values. THIS GOES ON THE RASPBERRY Pi
"""

import numpy as np
#from matplotlib import image
import time
#import matplotlib.pyplot as plt
from skimage import io
import socket
import pickle
from ServoPi_Minimal_2 import PWM
import os # lets us run a terminal command from python script (must run script from terminal using ./script.py)

#Enabling PWM output
    
# create an instance of the PWM class on i2c address 0x40
pwm = PWM(0x40)
# Set PWM frequency to 1.526 Khz and enable the output
pwm.set_pwm_freq(1526)
pwm.output_enable()
#start=time.time()
def read_in_img(filename,i,j):
    pixel_values= io.imread(filename, as_gray=True)
    pixel_values=pixel_values*255
    total_pix_vals=np.sum(pixel_values)
    max_pix_val=np.max(pixel_values)
    while total_pix_vals<500000 or max_pix_val>=255:
        time.sleep(2.0)
        take_pic='fswebcam -r 1280x720 --no-banner /home/pi/Test_Image_std/focal_%i_%i.jpg'%(i,j)
        os.system(take_pic)
        pixel_values= io.imread('/home/pi/Test_Image_std/focal_%i_%i.jpg'%(i,j), as_gray=True)
        pixel_values=pixel_values*255
        total_pix_vals=np.sum(pixel_values)
        max_pix_val=np.max(pixel_values)
        
    # pixel_values = np.array(image.imread(filename))
    #y_max=len(pixel_values)#rows
    #x_max=len(pixel_values[0])#columns
    #plt.imshow(pixel_values)
    #pixel_values=np.delete(pixel_values,np.s_[y_max-20:y_max],0) #removes bottom 20 pixels where the baanner is 
    return pixel_values

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


def read(filename,cornersize,i,j):
    
    
    pixels=read_in_img(filename,i,j)
    y_max=len(pixels)#rows
    x_max=len(pixels[0])#columns
    '''
    This is needed as imread will not do maths properly on any pixel 
    image reading will now output focal spot with background corrected
    and a metric that correlates to shape of focal spot only
    '''
    pixel_true=np.zeros((len(pixels),len(pixels[0])))#NEEDED AS THIS WILL NOT BE ABLE TO HANDLE MATHS OTHERWISE
    pixel_true[0:len(pixels),0:len(pixels[0])]=pixels[0:len(pixels),0:len(pixels[0])] #NEEDED 
    

    
    corners=corners_av(pixels,cornersize)
    grads=grad(corners,pixels)
    
   
    pixels_coord=np.mgrid[0:y_max,0:x_max].reshape(2,-1).T
    
   
    pixels_coord=(pixels_coord[0:len(pixels_coord),0]*grads[0]+pixels_coord[0:len(pixels_coord),1]*grads[1])+corners[0]
    pixel_background=pixels_coord.reshape(y_max,x_max)
    pixel_true=np.round(pixel_true-pixel_background)
   
    total_pixels=np.sum(pixels)
   
   
    fitness_parameter=np.sum(pixel_true**2)/(total_pixels)

    #end=time.time()
    #print(end-start)
    #print(fitness_parameter)
    # plt.imshow(pixel_true)
    return fitness_parameter,total_pixels
def all_channels_off():  #  Set channels 1-16 to off
    for count in range(1, 17, 1):
        pwm.set_pwm(count, 0, 0)

def main():
    
    #Client-Server connection
    
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket object
    host= '129.31.137.73' #pi IP address
    port=1234
    s.bind((host, port)) # bind socket to rasp pi IP adress and port number
    s.listen(5) #server will listen for clients, it has a queue of 5 in case too many connections at once
    print('Waiting for connection')
    clientsocket,address=s.accept() # accepts connection from client and saves client socket object and client's/our desktop's IP adress
    print('Got connection from',address)
    
    #Receiving actuator values from GA(Desktop)
    client_message=clientsocket.recv(10**6)#receive message from client
    client_message_p=pickle.loads(client_message)#unpickle object
    fitness_params=np.zeros((1,100))
    total_pixels=np.zeros((1,100))
    for i in range(1):
        actuator_values=client_message_p[i]    
        all_channels_off()
        time.sleep(1.0)
        print("actuator values = ",actuator_values)
        pwm.set_pwm(1, 0, actuator_values[0])
        pwm.set_pwm(2, 0, actuator_values[1])
        pwm.set_pwm(3, 0, actuator_values[2])
        pwm.set_pwm(4, 0, actuator_values[3])
        pwm.set_pwm(5, 0, actuator_values[4])
        
        
        for j in range(50):
            time.sleep(2.0)
            #send command to take focal spot picture
            take_pic='fswebcam -r 1280x720 --no-banner /home/pi/Test_Image_std/focal_%i_%i.jpg'%(i,j)
            os.system(take_pic)
            fitness_params[i][j],total_pixels[i][j]=read('/home/pi/Test_Image_std/focal_%i_%i.jpg'%(i,j),19,i,j)
            
    #send fit_params to desktop(GA)
        
    msg=pickle.dumps(fitness_params)
    clientsocket.send(msg)
    msg_1=pickle.dumps(total_pixels)
    clientsocket.send(msg_1)
    

    
    
    return
main()



