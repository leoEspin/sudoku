from copy import deepcopy
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

def update_value(
    index: tuple, 
    fill: int,
    board: np.array, 
    candidates: dict, 
)-> np.array:
    '''
    fill board at index with a valid  value and update relevant entries
    in candidates
    '''
    candidates = deepcopy(candidates)
    board[index] = fill
    indices_to_check = get_affected_indices(index, board.shape[0])
    for tup in indices_to_check:
        if tup in candidates and fill in candidates[tup]:
            candidates[tup].remove(fill)
    return board, {
        key:candidates[key] for key in candidates.keys() if len(candidates[key]) > 0\
            and key != index
        }

def fill_singles(board: np.array, candidates: dict)-> tuple:
    singles = False
    for tup in candidates:
        if len(candidates[tup]) == 1:
            singles = True
            break
    if singles:
        return fill_singles(*update_value(tup, candidates[tup][0], board, candidates))
    else:
        return board, candidates

def is_viable(board: np.array, candidates: dict):
    '''is board viable, meaning theres no empty position with no candidates'''
    indices = [tup for tup in get_indices(board.shape[0]) if board[tup] == 0]
    return len(
        [key for key in indices if key not in candidates.keys()]
    ) == 0

def count_empties(board: np.array)-> int:
    inds = get_indices(board.shape[0])
    return len([1 for x in inds if board[x] == 0])

def fill_board(
    board: np.array, 
    candidates: dict, 
)-> bool:
    print(candidates)
    if count_empties(board) == 0:
        return True
    if not is_viable(board, candidates):
        return False
    position, values = candidates.popitem()
    for i in range(len(values)):
        fill = values[i]
        print(position, fill)
        print(board)
        if fill_board(*update_value(position, fill, board, candidates)):
            return True
        board[position] = 0
    return False


if __name__ == '__main__':
    board = load_board(
        '5...8..49...5...3..673....115..........2.8..........187....415..3...2...49..5...3'
    )
    candidates = get_candidates(board)
    out = fill_board(board, candidates)
    if out:
        print(board)