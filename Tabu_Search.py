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
import random
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
x_init = x_curr[:]
f_curr = evaluate(x_curr)    #f_curr will hold the evaluation of the current soluton 
f_best = f_curr[:]


short_term = [0] * n # Initializes short term memory to 0 for all items
long_term = [0] * n  # Same as short term
tabu = False         # No moves are tabu initially

# Will compare previous solution and current to see what elements changed
# This is just a static short term memory, makes items tabu-active for
# five iterations.

def update_short(old,new):
    
    global short_term                # So memory can be updated outside of func.
    global tabu
    
    tabu = False 
    
    for i in range(len(old)):        # testing short-term memory
        if old[i] != new[i] and short_term[i] == 0:
            short_term[i] = 5
            tabu = True # This move is not allowed
        elif short_term[i] > 0:
            short_term[i] = short_term[i] - 1
            tabu = True
            

def update_long(solution):
    
    global long_term
    
    
    for i in range(len(solution)):
        long_term[i] = long_term[i] + solution[i]
        # Should count how many solutions have this item
 

# Will count the differences in solutions and store position of differences       
def difference(x,y):        
    different = []
    count = 0
    for i in range(len(x)):
        different.append(0)
        if x[i] != y[i]:
            count = count +1
            different[i] = 1
            
    return different, count

# Will give the neighborhood for relinking purposes
def relink_neigh(x, diff): # Takes in a solution and where the differences are
    
    nbrhood = []     
    
    for i in range(0,n):
        nbrhood.append(x[:])
        if nbrhood[i][i] == 1 and diff[i] == 1:
            nbrhood[i][i] = 0
        elif nbrhood[i][i] == 0 and diff[i] == 1:
            nbrhood[i][i] = 1
      
    return nbrhood
    
    
#begin local search overall logic ----------------

done = 0
    
while done == 0:
            
    Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr
    
    x_cand = random.choice(Neighborhood)  # Pick a random candidate solution
    
    update_short(x_curr, x_cand)
    solutionsChecked = solutionsChecked + 1
    
    # f_star is an update evalution function, taking into account how often items are
    # or are not in the bag. 
    f_star = evaluate(x_cand)[0] + np.dot(long_term,x_curr) 
    
    if tabu == False or f_star > f_best[0]: # Will accept if not tabu move or better than best
        x_curr = x_cand[:]
        f_curr = evaluate(x_cand)[:]
        update_long(x_curr)

    
    if evaluate(x_cand)[0] > f_best[0]:  # if there were no improving solutions in the neighborhood
        x_best = x_cand[:]              # Update the current best values and solutions
        f_best = evaluate(x_cand)[:]
    
    if solutionsChecked == 5000:
        done = 1
    
        
        print ("\nTotal number of solutions checked: ", solutionsChecked)
        print ("Best value found so far: ", f_best)        
    
print ("\nFinal number of solutions checked: ", solutionsChecked)
print ("Best value found: ", f_best[0])
print ("Weight is: ", f_best[1])
print ("Total number of items selected: ", np.sum(x_best))
print ("Best solution: ", x_best)
