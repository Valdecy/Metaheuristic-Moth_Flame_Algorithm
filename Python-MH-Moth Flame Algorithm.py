############################################################################

# Created by: Prof. Valdecy Pereira, D.Sc.
# UFF - Universidade Federal Fluminense (Brazil)
# email:  valdecy.pereira@gmail.com
# Course: Metaheuristics
# Lesson: Moth Flame Algorithm

# Citation: 
# PEREIRA, V. (2018). Project: Metaheuristic-Moth_Flame_Algorithm, File: Python-MH-Moth Flame Algorithm.py, GitHub repository: <https://github.com/Valdecy/Metaheuristic-Moth_Flame_Algorithm>

############################################################################

# Required Libraries
import pandas as pd
import numpy  as np
import random
import math
import os

# Function: Initialize Variables
def initial_moths(swarm_size = 3, min_values = [-5,-5], max_values = [5,5]):
    position = pd.DataFrame(np.zeros((swarm_size, len(min_values))))
    position['Fitness'] = 0.0
    for i in range(0, swarm_size):
        for j in range(0, len(min_values)):
             position.iloc[i,j] = random.uniform(min_values[j], max_values[j])
        position.iloc[i,-1] = target_function(position.iloc[i,0:position.shape[1]-1])
    return position

# Function: Update Flames
def update_flames(flames, position):
    population = pd.concat([flames, position])
    flames = population.nsmallest(flames.shape[0], "Fitness").copy(deep = True)
    return flames

# Function: Update Position
def update_position(position, flames, flame_number = 1, b_constant = 1, a_linear_component = 1, min_values = [-5,-5], max_values = [5,5]):
    for i in range (0, position.shape[0]):
        for j in range(0, len(min_values)):
            if (i <= flame_number):
                flame_distance = abs(flames.iloc[i,j] - position.iloc[i,j])
                b_constant = b_constant
                rnd_1 = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
                rnd_2 = (a_linear_component - 1)*rnd_1 + 1 
                position.iloc[i,j] = flame_distance*math.exp(b_constant *rnd_2)*math.cos(rnd_2*2*math.pi) + flames.iloc[i,j]    
            elif(i > flame_number):
                flame_distance = abs(flames.iloc[i,j] - position.iloc[i,j])
                b_constant = b_constant
                rnd_1 = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
                rnd_2 = (a_linear_component - 1)*rnd_1 + 1 
                position.iloc[i,j] = flame_distance*math.exp(b_constant *rnd_2)*math.cos(rnd_2*2*math.pi) + flames.iloc[flame_number,j]
            if (position.iloc[i, j] > max_values[j]):
                position.iloc[i, j] = max_values[j]
            elif (position.iloc[i, j] < min_values[j]):
                position.iloc[i, j] = min_values[j]
        position.iloc[i, -1] = target_function(position.iloc[i, 0:position.shape[1]-1])
    return position

# MFA Function
def moth_flame_algorithm(swarm_size = 3, min_values = [-5,-5], max_values = [5,5], generations = 50, b_constant = 1):
    position = initial_moths(swarm_size = swarm_size, min_values = min_values, max_values = max_values)
    flames   = position.nsmallest(position.shape[0], "Fitness").copy(deep = True)
    count = 0
    best_moth = flames.iloc[0,:].copy(deep = True)
    
    while (count <= generations):
        print("Generation: ", count, " of ", generations, " f(x) = ", best_moth[-1])
        
        flame_number = round(position.shape[0] - count*((position.shape[0] - 1)/generations))
        a_linear_component = -1 + count*((-1)/generations)
        position = update_position(position, flames, flame_number = flame_number, b_constant = b_constant, a_linear_component = a_linear_component, min_values = min_values, max_values = max_values)
        flames = update_flames(flames, position)
        count = count + 1
        if (flames.iloc[0,:][-1] < best_moth[-1]):
            best_moth = flames.iloc[0,:].copy(deep = True)
            
    print(best_moth)
    return best_moth

######################## Part 1 - Usage ####################################

# Function to be Minimized. Solution ->  f(x1, x2) = -1.0316; x1 = 0.0898, x2 = -0.7126 or x1 = -0.0898, x2 = 0.7126
def target_function (variables_values = [0, 0]):
    func_value = 4*variables_values[0]**2 - 2.1*variables_values[0]**4 + (1/3)*variables_values[0]**6 + variables_values[0]*variables_values[1] - 4*variables_values[1]**2 + 4*variables_values[1]**4
    return func_value

mfa = moth_flame_algorithm(swarm_size = 20, min_values = [-5,-5], max_values = [5,5], generations = 1000, b_constant = 1)
