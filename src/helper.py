import numpy as np
from game import S, H, B


def ship_sunk(grid, col, ind):
    # LIMITATION: Ships should be separated by other ships by blank cell. ships cannot be
    # placed in adjacent cols or rows. (just to make it work for now.)
    c = list(grid.columns).index(col)
    r = list(grid.index).index(ind)
    pos = []
    arr = grid.to_numpy()
    _close_by(arr, r, c, 'H+', pos)
    _close_by(arr, r, c, 'H-', pos)
    _close_by(arr, r, c, 'V+', pos)
    _close_by(arr, r, c, 'V-', pos)
    return np.all(np.array([arr[p] for p in pos]) == H)


def _close_by(array, row, col, dir, pos):
    if (row < 0 or row >= len(array)
            or col < 0 or col >= len(array[0])
            or array[row, col] == B):
        return False
    if array[row, col] != B and (row, col) not in pos:
        pos.append((row, col))
    if dir == 'H+':
        if array[row, col] != B \
                and _close_by(array, row, col + 1, dir, pos):
            pos.append((row, col))
            return True
    if dir == 'H-':
        if array[row, col] != B \
                and _close_by(array, row, col - 1, dir, pos):
            pos.append((row, col))
            return True
    if dir == 'V+':
        if array[row, col] != B \
                and _close_by(array, row + 1, col, dir, pos):
            pos.append((row, col))
            return True
    if dir == 'V-':
        if array[row, col] != B \
                and _close_by(array, row - 1, col, dir, pos):
            pos.append((row, col))
            return True


def all_ships_sunk(grid):
    arr = grid.to_numpy()
    return np.all(arr != S)
