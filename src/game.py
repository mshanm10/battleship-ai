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
    "name": "Player A",
    "ocean_grid": oc_grid.copy(),
    "targeting_grid": tg_grid.copy()
}
player_b = {
    "name": "Player B",
    "ocean_grid": oc_grid.copy(),
    "targeting_grid": tg_grid.copy()
}


def play(player, opponent):
    print(f"--------{player['name']}'s Targeting Grid---------")
    print(f"{player['targeting_grid']}")
    # print(other_player['ocean_grid'])
    move = input(f"{player['name']}'s attack (eg:A1)):").upper()
    col = move[0]
    ind = int(move[1:])
    # print(move)
    val = opponent['ocean_grid'][col][ind]
    if val == S:
        player['targeting_grid'][col][ind] = H
        opponent['ocean_grid'][col][ind] = H
        if hl.ship_sunk(opponent['ocean_grid'], col, ind):
            if hl.all_ships_sunk(opponent['ocean_grid']):
                print(f"{player['name']} Won  !!!!!!!!!!!!!!!!!!!")
                return False
            else:
                print('\/ \/ \/ \/ Ship Sunk \/ \/ \/ \/')
        else:
            print('* * * * * * * Hit * * * * * * * * ')
    else:
        print('- - - - -  - Miss - - - - - - - - ')
        player['targeting_grid'][col][ind] = M
    return True


if __name__ == '__main__':
    print("Battleship Game Started.")
    game_over = False
    player = player_a
    opponent = player_b
    while play(player, opponent):
        player, opponent = opponent, player
    print(f"Thanks for defending PicnicHealth")


