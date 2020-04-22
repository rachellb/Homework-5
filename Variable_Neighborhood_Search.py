
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
import random
import time # So program doesn't run forever

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
k = 1   # Which neighborhood structure we are using 
k_max = 3 # Number of neighborhood structures being used

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
          
       
# This takes in which neighborhood structure to use along with which solution
# to generate neighborhood from
    
def neighborhood(struct, x):    
        
    nbrhood = []     
    
    if struct == 1:             # 1-flip neighborhood
        for i in range(0,n):
            nbrhood.append(x[:])
            if nbrhood[i][i] == 1:
                nbrhood[i][i] = 0
            else:
                nbrhood[i][i] = 1
      
        return nbrhood
          
    elif struct == 2:           # 2-flip neighborhood
        index = 0
        
        for i in range(0,n-1):
            nbrhood.append(x[:])
            if nbrhood[index][i] == 1:
                nbrhood[index][i] = 0
            else:
                nbrhood[index][i] = 1
                
            for y in range(i,n-2):  # Appends neighborhood with the i^th element changed
                nbrhood.append(list(nbrhood[index]))
                
            for j in range(i+1,n):  # Goes down the list changing each element one by one, starting with i+1
                
            
                if nbrhood[index][j] == 1:
                    nbrhood[index][j] = 0
                else:
                    nbrhood[index][j] = 1
                index = index + 1
            
                    
        return nbrhood

    elif struct == 3:           # 3-flip neighborhood
      
    
        for i in range(0,n-2):
            neighbor = x[:]         # Make a copy of the solution
            
            if neighbor[i] == 1:
                neighbor[i] = 0
            else:
                neighbor[i] = 1
                 
            for j in range(i+1,n-1):
                neighbor2 = neighbor[:]
                if neighbor2[j] == 1:
                    neighbor2[j] = 0
                else:
                    neighbor2[j] = 1
                    
                
                for z in range(j+1,n):
                    neighbor3 = neighbor2[:]
                    if neighbor3[z] == 1:
                        neighbor3[z] = 0
                    else:
                        neighbor3[z] = 1
                    
                    nbrhood.append(neighbor3)
            
      
        return nbrhood

#create the initial solution
def initial_solution():
    x = []   #i recommend creating the solution as a list
    
    #need logic here!
    for i in range(0,n):
        x.append(myPRNG.randint(0,1))           # Fills the bag randomly
        #x.append(0)                            # Completely fills bag
        
        
        
    return x





def var_n_d(x_curr,f_curr):
    
    global solutionsChecked
    k = 1       # Start at first neighborhood
    start = time.time()
    
    
    TIME = 60 # 2 minutes
    while k <= k_max:  # will run through all neighborhood structures until best found in all 3 
                
        Neighborhood = neighborhood(k, x_curr)   #create a list of all neighbors in the neighborhood of x_curr
        
        
        for s in Neighborhood:                #evaluate every member in the neighborhood of x_curr
            
            
            solutionsChecked = solutionsChecked + 1
        
            if Neighborhood.index(s) == 0:  # Just to get an initial best in neighborhood
                nx_best = s[:]              #Stores the best in the neighborhood
                nf_best = evaluate(s)[:]
            
            if time.time() > start + TIME: # It should spend only 1 min per neighborhood
                return nx_best
                break
            else:
                if evaluate(s)[0] > nf_best[0]:    # If current is better than neighborhood best
                    nx_best = s[:]                 #find the best member and keep track of that solution
                    nf_best = evaluate(s)[:]       #and store its evaluation  
        
        
        if nf_best[0] > f_curr[0]:             # If the best in this neighborhood is better than the current best         
            x_curr = nx_best[:]
            f_curr = nf_best[:]
            k = 1   # Start over from first neighborhood
            
        else:
            k = k + 1
        
            
            print ("\nTotal number of solutions checked: ", solutionsChecked)
            print ("Best value found so far: ", nf_best)   
            
    return nx_best
    

#varaible to record the number of solutions evaluated
solutionsChecked = 0

x_curr = initial_solution()  #x_curr will hold the current solution 
x_best = x_curr[:]           #x_best will hold the best solution 
f_curr = evaluate(x_curr)    #f_curr will hold the evaluation of the current soluton 
f_best = f_curr[:]



#begin local search overall logic ----------------
done = 0
k = 1

while f_curr[0] < 19000:
    
    
    while k <= k_max:
        Neighborhood = neighborhood(k,x_curr)
        s = random.choice(Neighborhood)
        s_star = var_n_d(s, evaluate(s)[:])
        if evaluate(s_star)[0] > f_curr[0]: # Greater than since this is an optimization problem
            x_curr = s_star[:]
            f_curr = evaluate(s_star)[:]
            k = 1
            print("k is ", k)  # For testing purposes
        else:
            k = k + 1
            print("k is ", k)



print ("\nFinal number of solutions checked: ", solutionsChecked)
print ("Best value found: ", f_curr[0])
print ("Weight is: ", f_curr[1])
print ("Total number of items selected: ", np.sum(x_curr))
print ("Best solution: ", x_curr)
