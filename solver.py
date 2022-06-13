import os
import platform
import time
from copy import deepcopy
import numpy as np

class sudoku():
    def __init__(self,N:int = 9):
        self.size = N
        self.board = np.zeros((9,9), dtype=int)
        self.indices = [(i, j) for i in range(N) for j in range(N)]
        self.cells = {index: self._get_cell(index) for index in self.indices}
        currOS = platform.system()
        if currOS == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
        #delay for screen output in seconds. Can be changed with setDelay
        self.delay = 0.05 
        self.show_board()

    def setDelay(self,secs):
        self.delay=secs
            
    def show_board(self):
        '''
        Prints the current status of the board on the screen
        '''
        output=[]
        row=['|'] + ['-' for k in range(self.size)] + ['|']
        hedge=['+'] + ['-' for k in range(self.size)] + ['+']
        output.append(hedge)
        for i in range(self.size):
            output.append(row.copy())
        output.append(hedge)    
        
        for tup in self.indices:
            #flipping vertically (rows) for visual representation:
            val = self.board[tup]
            output[1 + tup[0]][1 + tup[1]] = str(val) if val != 0  else '-'
            
        time.sleep(self.delay)
        #position cursor at top left corner
        print("\033[1;1H")
        for i in range(self.size + 2):
            #still have to join each row into single strings
            print(''.join(output[i]))
    
    def _list_to_array(self, k: int)-> tuple:
        '''from index of a flat list to coordinates in 2D array'''
        return k // self.size, k % self.size

    def load_board(self, initial: str)-> np.array:
        j= 0
        for k, char in enumerate(initial):
            if char == '.':
                pass
            else:
                i, j = self._list_to_array(k)
                self.board[i, j] = int(char)
        self.show_board()
        return

    def _get_cell(self, index: tuple):
        '''coordinates of index' sqrt(N)xsqrt(N) cell (default 3x3 )'''
        cell_size = int(np.sqrt(self.size))
        return (index[0] // cell_size, index[1] // cell_size)

    def _get_affected_indices(self, index: tuple)-> list:
        '''affected positions according to sudoku rules'''
        rows = {(index[0], j) for j in range(self.size)}
        cols = {(j, index[1]) for j in range(self.size)}
        cell = {
            (i, j)  for i in range(self.size) for j in range(self.size)\
                if self.cells[(i, j)] == self.cells[index]
        }
        return list(
            rows.union(cols).union(cell)
        )
    
    def _get_occupied_vals(self, index: tuple)-> list:
        '''what are the used values according to sudoku rules'''
        values = {self.board[tup] for tup in self._get_affected_indices(index)}
        return [x for x in values if x != 0]

    def get_candidates(self)-> dict:
        '''board element at index is empty (0)'''
        candidates = {}
        for index in self.indices:
            if self.board[index] == 0:
                candidates[index] = [
                    x for x in range(1, 10) if x not in self._get_occupied_vals(index)
                ]
        return candidates

    def update_value(
        self,
        index: tuple, 
        fill: int,
        candidates: dict, 
    )-> np.array:
        '''
        fill board at index with a valid  value and update relevant entries
        in candidates
        '''
        candidates = deepcopy(candidates)
        self.board[index] = fill
        self.show_board()
        indices_to_check = self._get_affected_indices(index)
        for tup in indices_to_check:
            if tup in candidates and fill in candidates[tup]:
                candidates[tup].remove(fill)
        return {
            key:candidates[key] for key in candidates.keys() if len(candidates[key]) > 0\
                and key != index
        }
    
    def is_viable(self, candidates: dict):
        '''is board viable, meaning theres no empty position with no candidates'''
        indices = [tup for tup in self.indices if self.board[tup] == 0]
        return len(
            [key for key in indices if key not in candidates.keys()]
        ) == 0    

    def _count_empties(self)-> int:
        return len([1 for x in self.indices if self.board[x] == 0])

    def fill_board(self, candidates: dict = None)-> bool:
        if self._count_empties() == 0:
            return True
        if candidates == None:
            candidates = self.get_candidates()
        if not self.is_viable(candidates):
            return False
        position, values = candidates.popitem()
        for i in range(len(values)):
            fill = values[i]
            if self.fill_board(self.update_value(position, fill, candidates)):
                return True
            self.board[position] = 0
            self.show_board()
        return False


# def fill_singles(board: np.array, candidates: dict)-> tuple:
#     singles = False
#     for tup in candidates:
#         if len(candidates[tup]) == 1:
#             singles = True
#             break
#     if singles:
#         return fill_singles(*update_value(tup, candidates[tup][0], board, candidates))
#     else:
#         return board, candidates








if __name__ == '__main__':
    test = sudoku()
    test.load_board(
        '5...8..49...5...3..673....115..........2.8..........187....415..3...2...49..5...3'
    )
    test.fill_board()