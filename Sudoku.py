# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 20:51:04 2021

@author: Magnus Frandsen
"""

import numpy as np

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
                
                row = A[i,:]
                col = A[:,j]
                
                cube_row = i // 3
                cube_col = j // 3
                cube = A[3*cube_row:3*(cube_row+1),3*cube_col:3*(cube_col+1)].flatten()
                
                row_col_cube = np.array([row, col, cube]).reshape((len(row)*3))
                row_col_cube = np.unique(row_col_cube)
                
                tmp_possibilities = np.arange(1,10)[np.isin(np.arange(1,10),row_col_cube, assume_unique=True, invert = True)]
                tmp_n_possibilities = len(tmp_possibilities)     
                
                possibilities.append(tmp_possibilities)
                n_possibilities.append(tmp_n_possibilities)
                
                if tmp_n_possibilities == 1:
                    A[i,j] = tmp_possibilities[0]
                    print("Insert", i,j, tmp_possibilities[0]) if debug_print else None
                    n += 1
                elif tmp_n_possibilities == 0:
                    return possibilities, n_possibilities, False
    return possibilities, n_possibilities, True

class SudokuSolver():
    def __init__(self, start_grid):
        self.start_grid = start_grid
    
    def find_solution(self, debug_print = False):
        A = np.array(self.start_grid) #Current grid
        
        #First run
        possibilities, n_possibilities, success = run_singles(A)
                
        #Lists for saving guess information
        guess_idxs = []
        guess_rest_possibilities = []
        As = []
                
        for i in range(10000):
            if np.sum(A) == 405:
                break
            
            if success is True:
                As.append(np.array(A)) #Save A before making a guess
                guess_idx = np.argmin(n_possibilities) #Best guess idx
                tmp_possibilities = list(possibilities[guess_idx]) #Possibilities at guess_idx
                guess = tmp_possibilities.pop(0) #Guess
                
                #Save guess idx and guess
                guess_idxs.append(guess_idx)
                guess_rest_possibilities.append(tmp_possibilities)
                
            else: #If fail then take a step back in guesses
                print("Step back") if debug_print else None
                
                for j in range(len(guess_rest_possibilities)):
                    tmp_rest_poss = guess_rest_possibilities[-1]
                    if len(tmp_rest_poss) == 0: #Take another step back in guesses
                        print("Step back") if debug_print else None
                        guess_rest_possibilities.pop(-1)
                        guess_idxs.pop(-1)
                        As.pop(-1)
                    else: #Make another guess and revert to older grid
                        A = np.array(As[-1]) 
                        guess_idx = guess_idxs[-1]
                        guess = tmp_rest_poss.pop(-1)
                        break
                                      
            #Make guess
            print("Round:", i, "Sum:", np.sum(A), "Guess", (guess, guess_idx)) if debug_print else None
            A[guess_idx // 9, guess_idx % 9] = guess
            
            #Run singles
            possibilities, n_possibilities, success = run_singles(A, debug_print = False)
        
        if np.sum(A) == 405:
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
        solver = SudokuSolver(sudoku)
        solution = solver.find_solution(debug_print = True)
        print("Solution to {}. puzzle:\n".format(i), solution)

if __name__ == '__main__':
    main()
