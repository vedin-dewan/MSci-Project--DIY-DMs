# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 10:37:06 2021

@author: maxim
"""

import numpy as np
import time 

#GA Parameters
no_individs=8 #number of individuals in the populations i.e. number of test mirror surfaces in each generation
no_parents=4
max_it=20000

# Variables
no_genes=5 #number of genes in each individual i.e. no. of actuators on mirror
low_lim=0
up_lim=4096# range of possibe values for each gene i.e. PWM values for wach actuator 0-4095(randint does not include highest value)
best_sol_param=np.array([np.inf]) #as trying to minimize, if trying to maximize then 0
best_sol=np.zeros((1,no_genes)) # saves current best solution found

# Sphere Test/Fitness Function
def fitness_func(x):
    return sum(x**2)

# Generating Initial Population: Currently generating randomly, will optimize later
def init_pop(no_indivs,no_genes,low_lim,up_lim):
    pop_size=(no_individs,no_genes) #size of population
    new_pop=np.random.randint(low=low_lim, high=up_lim, size=pop_size)#includes low but excludes high
    return new_pop



# Selecting the parents(fittest) individuals
def selection(new_pop):
    
    fit_params=np.zeros(no_individs) #calculating fitness params for population
    
    for i in range(no_individs):
        fit_params[i]=fitness_func(new_pop[i])
  
    
            
        if fit_params[i]<=best_sol_param:
            best_sol_param[0]=fit_params[i]
            best_sol[0]=new_pop[i]
         
    
    # print(fit_params)
    
    #selecting parents
    parents=np.zeros((no_parents,no_genes))
    fitness=fit_params.copy()
    for i in range(no_parents):
        parents[i]=new_pop[np.argmin(fitness)]
        fitness[np.argmin(fitness)]=np.inf #replace current min with inf so that 2nd most min is chosen next
        if best_sol_param[0]<=5:
            command='stop'
        if best_sol_param[0]>=5:
            command=None 
    return parents,fit_params,command #command and fit_params


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

def mutate(parents,offsprings,fit_params):
    s=fit_params
    for i in range(fit_params.size):
        if s[i] > 1000:
            s[i]= 1000
   
      
    for i in range(no_parents):
        mut_gene_ind=np.random.randint(0,no_genes)

        mut_gene_value_dec=np.random.normal(offsprings[i],s[i],5)
     
        mut_gene_value=int(np.round(mut_gene_value_dec[i]))
   
        offsprings[i,mut_gene_ind]=mut_gene_value
    return offsprings
    

# def mutate(offsprings):
#     for i in range(no_parents):
#         mut_gene_ind= np.random.randint(0,no_genes) #randomly chooses which gene to mutate
#         mut_gene_value=np.random.randint(low=low_lim, high=up_lim) #randomly chooses new value of gene
#         offsprings[i,mut_gene_ind]=mut_gene_value
        
#     return offsprings



# Solve
def main():
    
    #initialize population
    new_pop=init_pop(no_individs,no_genes,low_lim,up_lim)
    
    
    for generation in range(max_it):
        #select parents
        start=time.time()
        parents,fit_params,command=selection(new_pop)
    
        #produce offsprings
        offsprings=crossover(parents)
    
        #mutation
        #offsprings=mutate(parents)
        offsprings=mutate(parents,offsprings,fit_params)
        
        new_pop[0:no_parents, :] = parents
        new_pop[no_parents:, :] = offsprings
        if command == 'stop':
            print('finished')
            end=time.time()
            print(end-start)
            print(generation)
            break
        
    
        print(generation)
      
    
    return 
    
main()

print(best_sol_param, best_sol)
