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
import numpy  as np
import random
import math
import os

# Function
def target_function():
    return

# Function: Initialize Variables
def initial_moths(swarm_size = 3, min_values = [-5,-5], max_values = [5,5], target_function = target_function):
    position = np.zeros((swarm_size, len(min_values)+1))
    for i in range(0, swarm_size):
        for j in range(0, len(min_values)):
             position[i,j] = random.uniform(min_values[j], max_values[j])
        position[i,-1] = target_function(position[i,0:position.shape[1]-1])
    return position

# Function: Update Flames
def update_flames(flames, position):
    population = np.vstack([flames, position])
    flames     = np.copy(population[population[:,-1].argsort()][:flames.shape[0],:])
    return flames

# Function: Update Position
def update_position(position, flames, flame_number = 1, b_constant = 1, a_linear_component = 1, min_values = [-5,-5], max_values = [5,5], target_function = target_function):
    for i in range (0, position.shape[0]):
        for j in range(0, len(min_values)):
            if (i <= flame_number):
                flame_distance = abs(flames[i,j] - position[i,j])
                rnd_1          = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
                rnd_2          = (a_linear_component - 1)*rnd_1 + 1 
                position[i,j]  = flame_distance*math.exp(b_constant *rnd_2)*math.cos(rnd_2*2*math.pi) + flames[i,j]    
            elif(i > flame_number):
                flame_distance = abs(flames[i,j] - position[i,j])
                rnd_1          = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
                rnd_2          = (a_linear_component - 1)*rnd_1 + 1 
                position[i,j]  = np.clip((flame_distance*math.exp(b_constant *rnd_2)*math.cos(rnd_2*2*math.pi) + flames[flame_number,j]), min_values[j],  max_values[j])
        position[i, -1] = target_function(position[i, 0:position.shape[1]-1])
    return position

# MFA Function
def moth_flame_algorithm(swarm_size = 3, min_values = [-5,-5], max_values = [5,5], generations = 50, b_constant = 1, target_function = target_function):
    count     = 0
    position  = initial_moths(swarm_size = swarm_size, min_values = min_values, max_values = max_values, target_function = target_function)
    flames    = np.copy(position[position[:,-1].argsort()][:,:])
    best_moth = np.copy(flames[0,:])
    while (count <= generations):
        print("Generation: ", count, " of ", generations, " f(x) = ", best_moth[-1])
        flame_number       = round(position.shape[0] - count*((position.shape[0] - 1)/generations))
        a_linear_component = -1 + count*((-1)/generations)
        position           = update_position(position, flames, flame_number = flame_number, b_constant = b_constant, a_linear_component = a_linear_component, min_values = min_values, max_values = max_values, target_function = target_function)
        flames             = update_flames(flames, position)
        count = count + 1
        if (best_moth[-1] > flames[0, -1]):
            best_moth = np.copy(flames[0,:])         
    print(best_moth)
    return best_moth

######################## Part 1 - Usage ####################################

# Function to be Minimized (Six Hump Camel Back). Solution ->  f(x1, x2) = -1.0316; x1 = 0.0898, x2 = -0.7126 or x1 = -0.0898, x2 = 0.7126
def six_hump_camel_back(variables_values = [0, 0]):
    func_value = 4*variables_values[0]**2 - 2.1*variables_values[0]**4 + (1/3)*variables_values[0]**6 + variables_values[0]*variables_values[1] - 4*variables_values[1]**2 + 4*variables_values[1]**4
    return func_value

mfa = moth_flame_algorithm(swarm_size = 20, min_values = [-5,-5], max_values = [5,5], generations = 250, b_constant = 1, target_function = six_hump_camel_back)

# Function to be Minimized (Rosenbrocks Valley). Solution ->  f(x) = 0; xi = 1
def rosenbrocks_valley(variables_values = [0,0]):
    func_value = 0
    last_x = variables_values[0]
    for i in range(1, len(variables_values)):
        func_value = func_value + (100 * math.pow((variables_values[i] - math.pow(last_x, 2)), 2)) + math.pow(1 - last_x, 2)
    return func_value

mfa = moth_flame_algorithm(swarm_size = 200, min_values = [-5,-5,-5,-5], max_values = [5,5,5,5], generations = 5000, b_constant = 1, target_function = rosenbrocks_valley)
