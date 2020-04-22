# -*- coding: utf-8 -*-

#basic hill climbing search provided as base code for the DSA/ISE 5113 course
#author: Charles Nicholson

#NOTE: YOU MAY CHANGE ALMOST ANYTHING YOU LIKE IN THIS CODE.  
#However, I would like all students to have the same problem instance, therefore please do not change anything relating to:
#   random number generation
#   number of items (should be 150)
#   random problem instance
#   weight limit of the knapsack

#------------------------------------------------------------------------------

#Student name: Rachel Bennett
#Date: April 19, 2020


#need some python libraries
import copy
from random import Random   #need this for the random number generation -- do not change
import numpy as np
import math   # For exponentials

#to setup a random number generator, we will specify a "seed" value
#need this for the random number generation -- do not change
seed = 5113
myPRNG = Random(seed)

#to get a random number between 0 and 1, use this:             myPRNG.random()
#to get a random number between lwrBnd and upprBnd, use this:  myPRNG.uniform(lwrBnd,upprBnd)
#to get a random integer between lwrBnd and upprBnd, use this: myPRNG.randint(lwrBnd,upprBnd)

#number of elements in a solution
n = 150

#create an "instance" for the knapsack problem
value = []
for i in range(0,n):
    value.append(round(myPRNG.triangular(5,1000,200),1))
    
weights = []
for i in range(0,n):
    weights.append(round(myPRNG.triangular(10,200,60),1))
    
#define max weight for the knapsack
maxWeight = 1500

#change anything you like below this line ------------------------------------

#monitor the number of solutions evaluated
solutionsChecked = 0
penalty = max(weights)                # To penalize the solutions with total weight over the max weight 
T0 = 1000000000  # Large enough to allow move of value 0 from initial value
temp = T0       # Set temp to initial temperature
alpha = 0.99    # For the cooling schedule

#function to evaluate a solution x
def evaluate(x):
          
    a=np.array(x)
    b=np.array(value)
    c=np.array(weights)
    
    totalValue = np.dot(a,b)     #compute the value of the knapsack selection
    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection
    
    if totalWeight > maxWeight:
        totalValue = totalValue - (penalty*totalWeight-maxWeight) 

    return [totalValue, totalWeight]   #returns a list of both total value and total weight
          
       
#here is a simple function to create a neighborhood
#1-flip neighborhood of solution x         
def neighborhood(x):
        
    nbrhood = []     
    
    for i in range(0,n):
        nbrhood.append(x[:])
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1
      
    return nbrhood
          


#create the initial solution
def initial_solution():
    x = []   #i recommend creating the solution as a list
    
    #need logic here!
    for i in range(0,n):
        x.append(myPRNG.randint(0,1))           # Fills the bag randomly
        #x.append(1)                            # Completely fills bag
        
        
        
    return x

def probability(x,y):
    p = math.exp(-abs((x - y))/temp)
    return p    # Returns as a probability


def cool():    # Cooling schedule
    global temp  # so temp can be changed 
    
    temp = alpha*temp     # Basic cooling



#varaible to record the number of solutions evaluated
solutionsChecked = 0

x_curr = initial_solution()  #x_curr will hold the current solution 
x_best = x_curr[:]           #x_best will hold the best solution 
f_curr = evaluate(x_curr)    #f_curr will hold the evaluation of the current soluton 
f_best = f_curr[:]



#begin local search overall logic ----------------

    
while temp > 1:     # Repeat until temperature goes below 1
            
    Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr
    
    for s in Neighborhood:                #evaluate every member in the neighborhood of x_curr
        solutionsChecked = solutionsChecked + 1
        if evaluate(s)[0] > f_best[0]:   
            x_best = s[:]                 #find the best member and keep track of that solution
            f_best = evaluate(s)[:]       #and store its evaluation  
            
        else:
            sample = myPRNG.random()      # Sample a number between 0 and 1
            p = probability(f_best[0], evaluate(s)[0]) # generate probability
            if p > sample:                # If prob greater than sample, accept move
                x_best = s[:]
                f_best = evaluate(s)[:]  
                
    # Lets start with a cooling schedule set in advance
    # Static schedule
    if solutionsChecked % 10 == 0:    # Cools every 10 iterations
        cool()
            
    x_curr = x_best[:]
    f_curr = f_best[:]
            
            
print ("\nFinal number of solutions checked: ", solutionsChecked)
print ("Best value found: ", f_best[0])
print ("Weight is: ", f_best[1])
print ("Total number of items selected: ", np.sum(x_best))
print ("Best solution: ", x_best)           