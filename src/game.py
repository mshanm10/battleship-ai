import pandas as pd
import numpy as np
import helper as hl

tg_grid = pd.DataFrame(np.zeros((5, 5), dtype=int), columns=['A', 'B', 'C', 'D', 'E'], index=[1, 2, 3, 4, 5])
B = 0  # blank
S = 2  # ship
H = 1  # hit
M = -1  # miss
oc_grid = pd.DataFrame([[0, 0, 0, 0, S],
                        [0, 0, 0, 0, S],
                        [S, S, S, 0, S],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0]], columns=['A', 'B', 'C', 'D', 'E'], index=[1, 2, 3, 4, 5])
player_a = {
    "ocean_grid": oc_grid.copy(),
    "targeting_grid": tg_grid.copy()
}
player_b = {
    "ocean_grid": oc_grid.copy(),
    "targeting_grid": tg_grid.copy()
}


if __name__ == '__main__':
    print("Battleship Game Started.")
    print("Your Targeting Grid (Player A)")
    print("-----BEFORE------")
    print(player_a['targeting_grid'])
    print(player_b['ocean_grid'])
    move = input("Player A (your move):").upper()
    col = move[0]
    ind = int(move[1:])
    print(move)
    val = player_b['ocean_grid'][col][ind]
    if val == S:
        player_a['targeting_grid'][col][ind] = H
        player_b['ocean_grid'][col][ind] = H
        if hl.ship_sunk(player_b['ocean_grid'], col, ind):
            if hl.all_ships_sunk(player_b['ocean_grid']):
                print('Won')
            else:
                print('Ship Sunk')
        else:
            print('Hit')
    else:
        print('Miss')
        player_a['targeting_grid'][col][ind] = M
    print("-----AFTER------")
    print(player_a['targeting_grid'])
    print(player_b['ocean_grid'])
