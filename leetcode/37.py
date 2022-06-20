class Solution:
    def _list_to_array(self, k: int)-> tuple:
        '''from index of a flat list to coordinates in 2D array'''
        return k // self.size, k % self.size

    def load_board(self, initial: str):
        n = min(len(initial), self.size**2)
        for k in range(n):
            char = initial[k]
            if 47 < ord(char) < 58:
                i, j = self._list_to_array(k)
                self.board[i, j] = int(char)
            else:
                pass
        return

    def _get_cell(self, index: tuple):
        '''coordinates of index' sqrt(N)xsqrt(N) cell (default 3x3 )'''
        return (index[0] // self.cell_size, index[1] // self.cell_size)

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
        values = {self.board[tup[0]][tup[1]] for tup in self._get_affected_indices(index)}
        return [x for x in values if x != '.']

    def get_candidates(self)-> dict:
        '''acceptable values for each empty position in the board'''
        candidates = {}
        for index in self.indices:
            if self.board[index[0]][index[1]] == '.':
                candidates[index] = [
                    str(x) for x in range(1, 10) if str(x) not in self._get_occupied_vals(index)
                ]
        return candidates

    def update_value(
        self,
        index: tuple, 
        fill: int,
        candidates: dict, 
    ):
        '''
        fill board at index with a valid  value and update relevant entries
        in candidates
        '''
        candidotes = {key: candidates[key].copy() for key in candidates.keys()}
        self.board[index[0]][index[1]] = fill
        indices_to_check = self._get_affected_indices(index)
        for tup in indices_to_check:
            if tup in candidotes and fill in candidotes[tup]:
                candidotes[tup].remove(fill)
        return {
            key:candidotes[key] for key in candidotes.keys() if len(candidotes[key]) > 0\
                and key != index
        }
    
    def is_viable(self, candidates: dict):
        '''is board viable, meaning theres no empty position with no candidates'''
        indices = [tup for tup in self.indices if self.board[tup[0]][tup[1]] == '.']
        return len(
            [key for key in indices if key not in candidates.keys()]
        ) == 0    

    def _count_empties(self)-> int:
        return len([1 for x in self.indices if self.board[x[0]][x[1]] == '.'])

    def fill_board(self, candidates: dict = None)-> bool:
        if self._count_empties() == 0:
            return True
        if candidates == None:
            candidates = self.get_candidates()
        #candidates = self.fill_singles(candidates)
        if not self.is_viable(candidates):
            return False
        if len(candidates) > 0:
            position, values = candidates.popitem()
            for i in range(len(values)):
                fill = values[i]
                if self.fill_board(self.update_value(position, fill, candidates)):
                    return True
                self.board[position[0]][position[1]] = '.'
        else:
            return self._count_empties() == 0

    def fill_singles(self, candidates: dict)-> tuple:
        '''fills all positions where only one value is admissible'''
        singles = False
        for tup in candidates:
            if len(candidates[tup]) == 1:
                singles = True
                break
        if singles:
            return self.fill_singles(self.update_value(tup, candidates[tup][0], candidates))
        else:
            return candidates

    def solveSudoku(self, boardo) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        self.board = boardo
        self.size = 9
        self.cell_size = 3
        self.indices = [(i, j) for i in range(9) for j in range(9)]
        self.cells = {index: self._get_cell(index) for index in self.indices}
        if self.fill_board():
            boardo = self.board