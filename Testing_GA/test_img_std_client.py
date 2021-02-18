#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 19:25:36 2021

@author: vedindewan &max

-Testing the standard deviation of our fitness parameters for one set of PWM values
"""

import numpy as np
import socket      
import pickle
import time




    
client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
host = '129.31.137.73' 
port = 1234            
client_socket.connect((host, port))

#initialize population
new_pop=np.array([[0,0,0,0,0],[0,4000,0,4000,0],[4000,0,0,0,4000],[1800,1000,1000,3500,1000],[2000,2000,2000,2000,2000]])
client_message=pickle.dumps(new_pop)
client_socket.send(client_message)

data=b""    
while True:        
    message=client_socket.recv(10**9)
    if not message:break
    data+=message
fit_params=pickle.loads(data)#unpickles message    

    
# message_1=client_socket.recv(10**7)
# total_pixel_vals=pickle.loads(message_1)
        
#%% Save fit_params array as pickled file

y=pickle.dumps(fit_params)
np.save("test_std_0000",y)


