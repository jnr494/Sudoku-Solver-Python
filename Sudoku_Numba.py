# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 20:51:04 2021

@author: Magnus Frandsen
"""

import numpy as np
import numba as nb
import time

@nb.njit(parallel = False)
def nb_sum(A):
    return np.sum(A)

@nb.njit(parallel=False)
def nb_get_row_col_cube(A, i, j):
    row = A[i,:]
    col = A[:,j]
    
    cube_row = i // 3
    cube_col = j // 3
    cube = A[3*cube_row:3*(cube_row+1),3*cube_col:3*(cube_col+1)]
    
    row_col_cube = np.append(np.append(row,col),cube)
    return row_col_cube

@nb.njit(parallel=False)
def nb_get_possibilities(A, i, j):
    row_col_cube = nb_get_row_col_cube(A,i,j)
    
    pre_not_possibilities = np.zeros(10, dtype = np.int64)
    for i in range(len(row_col_cube)):
        tmp_number = row_col_cube[i]
        pre_not_possibilities[tmp_number] = tmp_number
     
    n_possibilities = 9 - np.count_nonzero(pre_not_possibilities)
    
    possibilities = np.zeros(n_possibilities, dtype = np.int64)
    count = 0
    for i in range(1,10):
        tmp_number = pre_not_possibilities[i]
        if tmp_number == 0:
            possibilities[count] = i
            count += 1
    
    return possibilities, n_possibilities

def run_singles(A, debug_print = False):
    #Check for singles
    run = 0
    n = 1
    while n > 0:
        print("Run:",run) if debug_print else None
        run += 1
        
        possibilities = []
        n_possibilities = []
        
        n = 0
        for i in range(9):
            for j in range(9):
                if A[i,j] != 0:
                    possibilities.append(0)
                    n_possibilities.append(10)
                    continue
                  
                tmp_possibilities, tmp_n_possibilities = nb_get_possibilities(A, i, j)

                if tmp_n_possibilities == 1:
                    A[i,j] = tmp_possibilities[0]
                    print("Insert", i,j, tmp_possibilities[0]) if debug_print else None
                    n += 1
                elif tmp_n_possibilities == 0:
                    return possibilities, n_possibilities, False
                
                possibilities.append(tmp_possibilities)
                n_possibilities.append(tmp_n_possibilities)
                
    return possibilities, n_possibilities, True

class SudokuSolver():
    def __init__(self, start_grid):
        self.start_grid = start_grid
    
    def find_solution(self, debug_print = False):
        guess, guess_idx = 0,0 
        A = np.array(self.start_grid) #Current grid
        
        #First run
        possibilities, n_possibilities, success = run_singles(A)
        #Lists for saving guess information
        guess_idxs = []
        guess_rest_possibilities = []
        As = []
                
        for i in range(50000): #Change range to increase "max_iter" (10000 should be enough for most puzzles)
            if nb_sum(A) == 405:
                break
            
            if success is True:
                As.append(np.array(A)) #Save A before making a guess
                guess_idx = np.argmin(n_possibilities) #Best guess idx
                tmp_possibilities = list(possibilities[guess_idx]) #Possibilities at guess_idx
                guess = tmp_possibilities.pop() #Guess
                
                #Save guess idx and guess
                guess_idxs.append(guess_idx)
                guess_rest_possibilities.append(tmp_possibilities)
                
            else: #If fail then take a step back in guesses
                print("Step back") if debug_print else None
                
                for j in range(len(guess_rest_possibilities)):
                    tmp_rest_poss = guess_rest_possibilities[-1]
                    if len(tmp_rest_poss) == 0: #Take another step back in guesses
                        print("Step back") if debug_print else None
                        guess_rest_possibilities.pop()
                        guess_idxs.pop()
                        As.pop()
                    else: #Make another guess and revert to older grid
                        A = np.array(As[-1]) 
                        guess_idx = guess_idxs[-1]
                        guess = tmp_rest_poss.pop()
                        break
                                      
            #Make guess
            print("Round:", i, "Sum:", np.sum(A), "Guess", (guess, guess_idx)) if debug_print else None
            A[guess_idx // 9, guess_idx % 9] = guess
            
            #Run singles
            possibilities, n_possibilities, success = run_singles(A, debug_print = False)
            
        if nb_sum(A) == 405:
            print("Success") if debug_print else None
            self.solved_grid = A
            return A
        else:
            print("Fail") if debug_print else None
            self.solved_grid = None
            return None

def main():
    A = np.array([
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
        ])
    
    B = np.array([
        [4,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,9,0,0,0],
        [0,0,0,0,0,0,7,8,5],
        [0,0,7,0,4,8,0,5,0],
        [0,0,1,3,0,0,0,0,0],
        [0,0,6,0,7,0,0,0,0],
        [8,6,0,0,0,0,9,0,3],
        [7,0,0,0,0,5,0,6,2],
        [0,0,3,7,0,0,0,0,0]])
    
    C = np.array([
        [8,0,0,1,0,0,6,2,0],
        [0,7,5,2,0,0,0,0,9],
        [0,0,1,0,8,7,5,0,0],
        [0,6,0,0,1,0,2,5,0],
        [0,8,0,0,0,2,0,7,1],
        [7,0,0,3,0,0,8,0,0],
        [0,0,7,8,0,0,3,0,0],
        [2,0,0,0,7,1,0,0,0],
        [1,0,0,5,0,0,0,0,8]])
    
    D = np.array([
        [0,0,0,0,0,0,6,8,0],
        [0,0,0,0,7,3,0,0,9],
        [3,0,9,0,0,0,0,4,5],
        [4,9,0,0,0,0,0,0,0],
        [8,0,3,0,5,0,9,0,2],
        [0,0,0,0,0,0,0,3,6],
        [9,6,0,0,0,0,3,0,8],
        [7,0,0,6,8,0,0,0,0],
        [0,2,8,0,0,0,0,0,0]])
    
    
    E = np.array([
        [0,0,0,0,0,0,6,0,0],
        [0,0,0,0,0,7,0,0,1],
        [2,0,8,0,0,0,0,4,0],
        [6,0,0,0,0,0,0,0,0],
        [0,5,1,4,0,9,0,0,0],
        [0,0,0,5,0,0,0,2,0],
        [0,0,4,0,0,0,0,5,0],
        [0,0,7,1,9,6,0,0,0],
        [0,8,0,0,0,0,3,0,0]
        ])
    
    F = np.array([
        [2,0,7,1,0,0,6,0,0],
        [0,0,0,0,0,0,0,3,0],
        [5,0,0,0,0,0,0,0,0],
        [1,8,0,0,9,0,0,0,0],
        [0,0,0,0,0,0,2,0,7],
        [0,0,0,0,6,0,0,0,0],
        [0,3,0,0,0,0,0,6,0],
        [0,0,0,2,0,5,0,0,0],
        [0,4,0,0,0,0,0,0,0]
        ])
    
    G = np.array([
        [0,0,0,0,0,2,0,6,0],
        [0,0,0,3,0,0,0,0,1],
        [4,0,0,0,0,0,7,0,0],
        [0,1,0,6,0,0,0,0,0],
        [0,0,0,0,7,0,2,0,0],
        [0,0,0,0,0,0,0,0,0],
        [2,0,7,0,4,0,0,0,0],
        [0,0,0,5,0,0,0,1,3],
        [8,0,0,0,0,0,0,0,0]
        ])
    
    sudokus = [A,B,C,D,E,F,G]
    
    for i, sudoku in enumerate(sudokus):
        start = time.time()
        solver = SudokuSolver(sudoku)
        solution = solver.find_solution(debug_print = False)
        stop = time.time()
        print("Solution to {}. puzzle ({} secs):\n".format(i,stop-start), solution)

if __name__ == '__main__':
    main()
