# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 22:25:32 2019

@author: Rudra
"""

import numpy as np
import matplotlib.pyplot as pyplot
import matplotlib.cm as cm
import random
import math


def generateGrid(dim, n):
    grid = np.zeros([dim, dim])
    
    for x in range(n):
        y = random.randint(1, 101)
        print(y)
        n = y-1
        k= n % 10
        n= int(n / 10)
        grid[n][k] = -1 #Defining the obstacle here 

    return grid

def assess_mines(grid, dim):
    for i in range(dim):
        for j in range(dim):
            if grid[i][j] != -1:
                count = 0
                if i == 0:
                    if j == 0:
                        if grid[i+1][j] == -1:
                            count+=1
                        if grid[i+1][j+1] == -1:
                            count+=1
                        if grid[i][j+1] == -1:
                            count+=1
                    elif j == dim-1:
                        if grid[i+1][j] == -1:
                            count+=1 
                        if grid[i+1][j-1] == -1:
                            count+=1
                        if grid[i][j-1] == -1:
                            count+=1
                    else:
                        if grid[i][j-1] == -1:
                            count+=1
                        if grid[i-1][j-1] == -1:
                            count+=1
                        if grid[i-1][j] == -1:
                            count+=1
                        if grid[i-1][j+1] == -1:
                            count+=1
                        if grid[i][j+1] == -1:
                            count+=1
                        
                        
                elif i == dim-1:
                    if j == 0:
                        if grid[i-1][j] == -1:
                            count+=1
                        if grid[i-1][j+1] == -1:
                            count+=1
                        if grid[i][j+1] == -1:
                            count+=1
                    elif j == dim-1:
                        if grid[i][j-1] == -1:
                            count+=1 
                        if grid[i-1][j-1] == -1:
                            count+=1
                        if grid[i-1][j] == -1:
                            count+=1
                    else:
                        if grid[i][j-1] == -1:
                            count+=1
                        if grid[i-1][j-1] == -1:
                            count+=1
                        if grid[i-1][j] == -1:
                            count+=1
                        if grid[i-1][j+1] == -1:
                            count+=1
                        if grid[i][j+1] == -1:
                            count+=1
              
                elif j == 0:
                    if grid[i-1][j] == -1:
                        count+=1
                    if grid[i-1][j+1] == -1:
                        count+=1
                    if grid[i][j+1] == -1:
                        count+=1
                    if grid[i+1][j+1] == -1:
                        count+=1
                    if grid[i+1][j] == -1:
                        count+=1
                        
                        
                elif j == dim-1:
                    if grid[i-1][j] == -1:
                        count+=1
                    if grid[i-1][j-1] == -1:
                        count+=1
                    if grid[i][j-1] == -1:
                        count+=1
                    if grid[i+1][j-1] == -1:
                        count+=1
                    if grid[i+1][j] == -1:
                        count+=1
                
                else:
                    if grid[i+1][j] == -1:
                        count+=1
                    if grid[i+1][j+1] == -1:
                        count+=1
                    if grid[i][j+1] == -1:
                        count+=1
                    if grid[i-1][j+1] == -1:
                        count+=1
                    if grid[i-1][j] == -1:
                        count+=1
                    if grid[i-1][j-1] == -1:
                        count+=1
                    if grid[i][j-1] == -1:
                        count+=1
                    if grid[i+1][j-1] == -1:
                        count+=1
                        
                grid[i][j]=count

    return grid
                        



    
dim = int(input("Enter the dimensions of the grid: "))
n = int(input("Enter the number of obstacles in the grid: "))
grid = generateGrid(dim, n)
print(np.matrix(grid)) 
print("\n\n")
data_grid = assess_mines(grid,dim)
print(np.matrix(data_grid)) 





