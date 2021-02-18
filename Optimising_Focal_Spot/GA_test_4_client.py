#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 19:25:36 2021

@author: vedindewan

-This is a test Genetic Algorithm(GA) to maximize focal spot parameter.

-This one has a convergence criteria

-New mutation using gaussian distribution (works 31 times faster )

- Also breaks if fitness param is as good as we need it 

- Sets up a client server connection with pi
"""
    
#%%

#Modules
import numpy as np
import socket      
import pickle
import time

#GA Parameters
no_individs=8 #number of individuals in the populations i.e. number of test mirror surfaces in each generation
no_parents=4
max_it=3

# Variables
no_genes=5 #number of genes in each individual i.e. no. of actuators on mirror
low_lim=0
up_lim=4096# range of possibe values for each gene i.e. PWM values for wach actuator 0-4095(randint does not include highest value)
conv_gens=20 #number of stale generations after which GA is stopped
best_possible=120

#values to save
best_sol_param=np.zeros(1) #as trying to minimize, if trying to maximize then 0
best_sol=np.zeros((1,no_genes)) # saves current best solution found
no_stale_gens=np.array([0]) # number of continuos generations with no/little change in fitness param





# Generating Initial Population: Currently generating randomly, will optimize later
def init_pop(no_indivs,no_genes,low_lim,up_lim):
    pop_size=(no_individs,no_genes) #size of population
    new_pop=np.random.randint(low=low_lim, high=up_lim, size=pop_size)#includes low but excludes high
    return new_pop


# print(new_pop)

# Selecting the parents(fittest) individuals
def selection(new_pop,fit_params):
    fit_params=fit_params
    
    #selecting parents
    parents=np.zeros((no_parents,no_genes))
    parents_fitness=np.zeros(no_parents)
    fitness=fit_params.copy()
    for i in range(no_parents):
        parents[i]=new_pop[np.argmax(fitness)]
        parents_fitness[i]=np.max(fitness)
        fitness[np.argmax(fitness)]=0 #replace current max with 0 so that 2nd most max is chosen next
        
       
    return parents,parents_fitness


# Crossover to produce offspring/children
def crossover(parents):
    
    alpha=np.random.randint(0,2,no_genes)#randomly generating mask of 0s and 1s
    offsprings=np.zeros((no_parents,no_genes))
    no_of_cross=np.int(no_parents/2)
    for i in range(no_of_cross):
        offsprings[i]= alpha*parents[i] + (1-alpha)*parents[no_parents-1-1*i]
        offsprings[no_parents-1-1*i]=(1-alpha)*parents[i] + alpha*parents[no_parents-1-1*i]
   
    return offsprings


# Mutation: Currently using a mutation rate of 20%(i.e one gene)
def mutate(parents,offsprings,parents_fitness):
    s=1/parents_fitness
    for i in range(len(parents_fitness)):
        if parents_fitness[i] >= 70:
            s[i]= s[i] * 5000
        else:
            s[i]= s[i] * 40000
   
      
    for i in range(no_parents):
        mut_gene_ind=np.random.randint(0,no_genes)

        mut_gene_value_dec=np.random.normal(offsprings[i],s[i])
     
        mut_gene_value=int(np.round(mut_gene_value_dec[i]))
        
        #if statement stops numbers being negative: takes negative values and turns them into absolute values (-10 -> 10)
        #need to test if setting to 0 is better or abs value
        if mut_gene_value < 0:
            mut_gene_value= np.absolute(mut_gene_value)
            # mut_gene_value= 0
        
        if mut_gene_value >4095:
            mut_gene_value=4095
   
        offsprings[i,mut_gene_ind]=mut_gene_value
    return offsprings



def converge(new_pop,fit_params):
    max_ind=np.argmax(fit_params)
   
    
    if  fit_params[max_ind]<=best_sol_param[0]:
        no_stale_gens[0]+=1
    else:
        no_stale_gens[0]=0
    #print(no_stale_gens[0])   
        
    if fit_params[max_ind]>=best_sol_param[0]:
            best_sol_param[0]=fit_params[max_ind]
    
            best_sol[0]=new_pop[max_ind]
    # if better than best fitness param then stop 
    if best_sol_param[0]>=best_possible:
            command='stop'
    if best_sol_param[0]<=best_possible:
            command=None 
    return command

# Solve
def main():
    start=time.time()
    client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
    host = '129.31.137.73' 
    port = 1234            
    client_socket.connect((host, port))
    
    #initialize population
    new_pop=init_pop(no_individs,no_genes,low_lim,up_lim)
    
    for generation in range(max_it):
        start_gen=time.time()
        print("NEW POP = ",new_pop)
        client_message=pickle.dumps(new_pop)
        client_socket.send(client_message)
        message=client_socket.recv(10**7)
        fit_params=pickle.loads(message)#unpickles message
        print("FIT_PARAM = ",fit_params)
        #select parents
        parents,parents_fitness=selection(new_pop,fit_params)
        
        #Convergence check
        command=converge(new_pop,fit_params)
        if no_stale_gens[0]==conv_gens:
            break
        
        if command == 'stop':
            print('finished')
            print(generation)
            break
    
        #produce offsprings
        offsprings=crossover(parents)
    
        #mutation
        offsprings=mutate(parents,offsprings,parents_fitness)

        
        new_pop[0:no_parents, :] = parents
        new_pop[no_parents:, :] = offsprings
        
        print(generation)
        end_gen=time.time()
        time_gen=end_gen-start_gen
        print("time_%i = "%generation, time_gen)
    #sending empty message to break loop
    empty_message=pickle.dumps([])
    client_socket.send(empty_message)
    empty=client_socket.recv(10**6)
    client_message=pickle.dumps(best_sol[0])
    client_socket.send(client_message)
    client_socket.close()  
    return 
start=time.time()    
main()
end=time.time()
print("time = ",end-start," seconds")
print("best solution is = ",best_sol[0])
print("final fitness parameter is = ",best_sol_param[0])

#%%






