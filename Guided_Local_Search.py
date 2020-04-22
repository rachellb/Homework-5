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
#Date: April 5, 2020


#need some python libraries
import copy
from random import Random   #need this for the random number generation -- do not change
import numpy as np


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
alpha = 1     # For tuning lambda 


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




#varaible to record the number of solutions evaluated
solutionsChecked = 0

x_curr = initial_solution()  #x_curr will hold the current solution 
x_best = x_curr[:]           #x_best will hold the best solution 
f_curr = evaluate(x_curr)    #f_curr will hold the evaluation of the current soluton 
f_best = f_curr[:]
x_worst = x_curr[:]          #x_best will hold local minimum
f_worst = evaluate(x_worst)  # will hold evaluation of local minimum
lbda = alpha * f_curr[0]/sum(x_curr)   # So that there's an initial lambda

p = [0] * n  # penalty vector
c = [0] * n  # cost vector


for i in range(len(weights)):   # cost of an item will be ratio of weight:value
    c[i] = weights[i]/value[i]  # Heavier items cost more, but high value offsets


def update_penalty(s):      # This will update the penalty function
    global p
    
    utility = [0] * n
    
    for i in range(len(utility)):
        utility[i] = s[i] * (c[i]/(1 + p[i])) # Calculates the utility of each object in solution
    
    m = max(utility) # Finds the max object
    penalize = [] # Will store which objects will be penalized
    [penalize.append(index) for index, value in enumerate(utility) if value == m]
    
    for i in range(len(p)):
        if i in penalize:    # if i is one of the items to be penalized
            p[i] = p[i] + 1  # add to it's penalty value
    

def neigh_search(x):    # Just searching for best in neighborhood
    
    global solutionsChecked
    global f_worst
    global lbda
    f_worst = evaluate(x)[:]    # Should reset f_worst to be neighborhood worst
    
    nx_best = []
    fn_best = []
    
    Neighborhood = neighborhood(x)
    
    for s in Neighborhood:
        solutionsChecked = solutionsChecked + 1
        
        if Neighborhood.index(s) == 0:
            nx_best = s[:]
            fn_best = evaluate(s)[:]
        
        else:
            if (evaluate(s)[0] + lbda*np.dot(s,p)) > (fn_best[0] + lbda*np.dot(nx_best,p)): # Evaluate by f*
                nx_best = s[:]
                fn_best = evaluate(s)[:]
                
        if evaluate(s)[0] < f_worst[0]:     # Finds the local minimum for lambda
            x_worst = s[:]
            f_worst = evaluate(s)[:]     
            lbda = alpha * f_worst[0]/sum(x_worst) # The formula for lambda 
        
        
    return nx_best
        
            
        


#begin local search overall logic ----------------


    
while solutionsChecked < 10000:
            
    s = neigh_search(x_curr)    # stores best in neighborhood
    s_star = evaluate(s)[0] + lbda * np.dot(s,p) # Finds s* evaluation with lbda
    curr_star = f_curr[0] + lbda *np.dot(x_curr,p)
    if s_star > curr_star:
        x_curr = s[:]
        f_curr = evaluate(x_curr)[:]
        
        if f_curr[0] > f_best[0]:
            x_best = x_curr[:]
            f_best = f_curr[:]
        
    else:
        update_penalty(x_curr)
    
        
        print ("\nTotal number of solutions checked: ", solutionsChecked)
        print ("Best value found so far: ", f_best)        
    
print ("\nFinal number of solutions checked: ", solutionsChecked)
print ("Best value found: ", f_best[0])
print ("Weight is: ", f_best[1])
print ("Total number of items selected: ", np.sum(x_best))
print ("Best solution: ", x_best)
