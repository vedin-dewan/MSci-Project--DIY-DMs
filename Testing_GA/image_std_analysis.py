#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 03:48:09 2021

@author: vedindewan
"""
import numpy as np
import socket      
import pickle
import time
import matplotlib.pyplot as plt



one=np.load("test_std_1_images.npy")       
fit_params_1=pickle.loads(one)
#print(fit_params_1)

two=np.load("test_std_2_images.npy")       
fit_params_2=pickle.loads(two)
#print(fit_params_2)

three=np.load("test_std_3_images.npy")       
fit_params_3=pickle.loads(three)
#print(fit_params_3)

four=np.load("test_std_4_images.npy")       
fit_params_4=pickle.loads(four)
#print(fit_params_4)

five=np.load("test_std_5_images.npy") 
fit_params_5=pickle.loads(five)
#print(fit_params_5)

six=np.load("test_std_6_images.npy") 
fit_params_6=pickle.loads(six)
#print(fit_params_6)

seven=np.load("test_std_7_images.npy") 
fit_params_7=pickle.loads(seven)
#print(fit_params_7)

eight=np.load("test_std_8_images.npy") 
fit_params_8=pickle.loads(eight)
#print(fit_params_8)

nine=np.load("test_std_9_images.npy") 
fit_params_9=pickle.loads(nine)
#print(fit_params_9)

ten=np.load("test_std_10_images.npy") 
fit_params_10=pickle.loads(ten)
print(fit_params_10)
fit_params=[fit_params_1,fit_params_2,fit_params_3,fit_params_4,fit_params_5,fit_params_6,fit_params_7,fit_params_8,fit_params_9,fit_params_10]

#%%
stds_fit=np.zeros((10,5,20))
mean=np.zeros((10,5,20))
no_images=np.array([1,2,3,4,5,6,7,8,9,10])
for i in range(10):
    for k in range(5):
        for j in range(20):
            stds_fit[i][k][j]=np.std(fit_params[i][k][j])
            mean[i][k][j]=np.mean(fit_params[i][k][j])
mean_1=np.array([np.mean(mean[0][0]),np.mean(mean[1][0]),np.mean(mean[2][0]),np.mean(mean[3][0]),np.mean(mean[4][0]),np.mean(mean[5][0]),np.mean(mean[6][0]),np.mean(mean[7][0]),np.mean(mean[8][0]),np.mean(mean[9][0])])
mean_2=np.array([np.mean(mean[0][1]),np.mean(mean[1][1]),np.mean(mean[2][1]),np.mean(mean[3][1]),np.mean(mean[4][1]),np.mean(mean[5][1]),np.mean(mean[6][1]),np.mean(mean[7][1]),np.mean(mean[8][1]),np.mean(mean[9][1])])
mean_3=np.array([np.mean(mean[0][2]),np.mean(mean[1][2]),np.mean(mean[2][2]),np.mean(mean[3][2]),np.mean(mean[4][2]),np.mean(mean[5][2]),np.mean(mean[6][2]),np.mean(mean[7][2]),np.mean(mean[8][2]),np.mean(mean[9][2])])
mean_4=np.array([np.mean(mean[0][3]),np.mean(mean[1][3]),np.mean(mean[2][3]),np.mean(mean[3][3]),np.mean(mean[4][3]),np.mean(mean[5][3]),np.mean(mean[6][3]),np.mean(mean[7][3]),np.mean(mean[8][3]),np.mean(mean[9][3])])
mean_5=np.array([np.mean(mean[0][4]),np.mean(mean[1][4]),np.mean(mean[2][4]),np.mean(mean[3][4]),np.mean(mean[4][4]),np.mean(mean[5][4]),np.mean(mean[6][4]),np.mean(mean[7][4]),np.mean(mean[8][4]),np.mean(mean[9][4])])

std_1=np.array([np.std(mean[0][0]),np.std(mean[1][0]),np.std(mean[2][0]),np.std(mean[3][0]),np.std(mean[4][0]),np.std(mean[5][0]),np.std(mean[6][0]),np.std(mean[7][0]),np.std(mean[8][0]),np.std(mean[9][0])])
std_2=np.array([np.std(mean[0][1]),np.std(mean[1][1]),np.std(mean[2][1]),np.std(mean[3][1]),np.std(mean[4][1]),np.std(mean[5][1]),np.std(mean[6][1]),np.std(mean[7][1]),np.std(mean[8][1]),np.std(mean[9][1])])
std_3=np.array([np.std(mean[0][2]),np.std(mean[1][2]),np.std(mean[2][2]),np.std(mean[3][2]),np.std(mean[4][2]),np.std(mean[5][2]),np.std(mean[6][2]),np.std(mean[7][2]),np.std(mean[8][2]),np.std(mean[9][2])])
std_4=np.array([np.std(mean[0][3]),np.std(mean[1][3]),np.std(mean[2][3]),np.std(mean[3][3]),np.std(mean[4][3]),np.std(mean[5][3]),np.std(mean[6][3]),np.std(mean[7][3]),np.std(mean[8][3]),np.std(mean[9][3])])
std_5=np.array([np.std(mean[0][4]),np.std(mean[1][4]),np.std(mean[2][4]),np.std(mean[3][4]),np.std(mean[4][4]),np.std(mean[5][4]),np.std(mean[6][4]),np.std(mean[7][4]),np.std(mean[8][4]),np.std(mean[9][4])])

plt.plot(no_images,(std_1/mean_1)*100,label="surface_1",linestyle="-",marker="x")
plt.plot(no_images,(std_2/mean_2)*100,label="surface_2",linestyle="-",marker="x")
plt.plot(no_images,(std_3/mean_3)*100,label="surface_3",linestyle="-",marker="x")
plt.plot(no_images,(std_4/mean_4)*100,label="surface_4",linestyle="-",marker="x")
plt.plot(no_images,(std_5/mean_5)*100,label="surface_5",linestyle="-",marker="x")

# mean=[np.mean(fit_params[4][0][0]),np.mean(fit_params[4][0][1]),np.mean(fit_params[4][0][0])]
plt.ylabel("Std. Dev. of fitness parameter (%)")

plt.xlabel("No. of Images Averaged Over")

plt.legend()
plt.grid()
plt.show()


#%%
fitness=np.load("test_std_0000.npy") 
fitness=pickle.loads(fitness)
mean=np.mean(fitness[0][0:50])
std=np.std(fitness[0][0:50])
std_percent=(std/mean)*100
print(mean,std_percent)






