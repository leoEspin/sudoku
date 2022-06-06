import numpy as np

def get_indices(N: int)-> list:
    return [(i, j) for i in range(N) for j in range(N)]

def list_to_array(k: int, N: int = 9)-> tuple:
    '''from index of a flat list to coordinates in 2D array'''
    return k // N, k % N

def load_board(initial: str, N: int = 9)-> np.array:
    board = np.zeros((9,9), dtype=int)
    j= 0
    for k, char in enumerate(initial):
        if char == '.':
            pass
        else:
            i, j = list_to_array(k, N)
            board[i, j] = int(char)
    return board

def get_cell(index: tuple, N: int = 9):
    '''coordinates of index' sqrt(N)xsqrt(N) cell (default 3x3 )'''
    cell_size = int(np.sqrt(N))
    return (index[0] // cell_size, index[1] // cell_size)

def get_affected_indices(index: tuple, N: int = 9)-> list:
    '''affected positions according to sudoku rules'''
    curr_cell = get_cell(index, N)
    rows = {(index[0], j) for j in range(N)}
    cols = {(j, index[1]) for j in range(N)}
    cell = {
        (i, j)  for i in range(N) for j in range(N)\
            if get_cell((i, j), N) == curr_cell
    }
    return list(
        rows.union(cols).union(cell)
    )
    
def get_occupied_vals(index: tuple, board: np.array, N: int = 9)-> list:
    '''what are the used values according to sudoku rules'''
    values = {board[tup] for tup in get_affected_indices(index, N)}
    return [x for x in values if x != 0]

def get_candidates(board: np.array, N: int = 9)-> dict:
    '''board element at index is empty (0)'''
    indices = get_indices(N)
    candidates = {}
    for index in indices:
        if board[index] == 0:
            candidates[index] = [
                x for x in range(1, 10) if x not in get_occupied_vals(index, board)
            ]
    return candidates

def update_value(index: tuple, board: np.array, candidates: dict)-> np.array:
    '''
    for an index with a valid answer, fill the answer value and update
    relevant candidates
    '''
    fill = candidates[index][0] # THE valid answer
    board[index] = fill
    indices_to_check = get_affected_indices(index, board.shape[0])
    for tup in indices_to_check:
        if tup in candidates and fill in candidates[tup]:
            candidates[tup].remove(fill)
    return board, {
        key:candidates[key] for key in candidates.keys() if len(candidates[key]) > 0
        }

def fill_board(
    board: np.array, 
    candidates: dict, 
    ncandidates: int =1,
    increase: bool = True
)-> bool:
    if len(candidates) == 0:
        return False
    for tup in candidates:
        if len(candidates[tup]) == ncandidates:
            increase = False
            break
    if increase:
        ncandidates += 1
        fill_board(board, candidates, ncandidates)
    print(ncandidates, tup, '\n', candidates)
    fill_board(*update_value(tup, board, candidates), ncandidates)
    return True


if __name__ == '__main__':
    board = load_board(
        '5...8..49...5...3..673....115..........2.8..........187....415..3...2...49..5...3'
    )
    candidates = get_candidates(board)
    out = fill_board(board, candidates)
    if out:
        print(board)