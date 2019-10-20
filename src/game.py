import pandas as pd
import numpy as np
import helper as hl
import datetime
import itertools
import random
import time

tg_grid = pd.DataFrame(np.zeros((5, 5), dtype=int), columns=['A', 'B', 'C', 'D', 'E'], index=[1, 2, 3, 4, 5])
B = 0  # blank
S = 2  # ship
H = 1  # hit
M = -1  # miss

SLEEP_SECS_BETWEEN_PLAYS = 0

def as_grid(nparray):
    return pd.DataFrame(nparray, columns=['A', 'B', 'C', 'D', 'E'], index=[1, 2, 3, 4, 5])


oc_grids = [as_grid([[0, 0, 0, 0, S],
                     [0, 0, 0, 0, S],
                     [S, S, S, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, S, S, S, S]]),

            as_grid([[0, S, 0, S, 0],
                     [0, S, 0, S, 0],
                     [0, S, 0, S, 0],
                     [0, 0, 0, S, 0],
                     [S, S, 0, 0, 0]]),

            as_grid([[0, 0, 0, 0, 0],
                     [S, S, S, S, 0],
                     [0, 0, 0, 0, S],
                     [0, 0, S, 0, S],
                     [0, 0, S, 0, S]]),

            as_grid([[0, 0, 0, 0, 0],
                     [S, 0, S, S, S],
                     [S, 0, 0, 0, 0],
                     [S, 0, 0, S, S],
                     [S, 0, 0, 0, 0]]),

            as_grid([[S, 0, 0, 0, S],
                     [S, 0, 0, 0, S],
                     [S, 0, 0, 0, 0],
                     [0, S, S, S, S],
                     [0, 0, 0, 0, 0]]),

            as_grid([[S, 0, S, 0, 0],
                     [S, 0, S, 0, 0],
                     [S, 0, 0, 0, 0],
                     [0, S, S, S, S],
                     [0, 0, 0, 0, 0]]),
            ]

random.shuffle(oc_grids)


def real_user():
    return input(f"{player['name']}'s attack (eg:A1)):").upper()


class RandomPlayer(object):

    def __init__(self, player):
        self.moves_available = list(itertools.product(tg_grid.columns, tg_grid.index))
        random.shuffle(self.moves_available)

    def input(self):
        print(f"{player['name']}'s attack (eg:A1)): random player playing...(please wait)")
        time.sleep(SLEEP_SECS_BETWEEN_PLAYS)
        return ''.join(map(str, self.moves_available.pop()))


player_a = {
    "name": "Player A",
    "ocean_grid": oc_grids[0].copy(),
    "targeting_grid": tg_grid.copy()
}
player_b = {
    "name": "Player B",
    "ocean_grid": oc_grids[1].copy(),
    "targeting_grid": tg_grid.copy()
}

WON = 'Won'
SHIP_SUNK = 'Ship Sunk'
HIT = 'Hit'
MISS = 'Miss'


def play(player, opponent, f_obj):
    print(f"--------{player['name']}'s Targeting Grid---------")
    print(f"{player['targeting_grid']}")
    move = player['get_input']()
    col = move[0]
    ind = int(move[1:])
    val = opponent['ocean_grid'][col][ind]
    status = None
    if val == S:
        player['targeting_grid'][col][ind] = H
        opponent['ocean_grid'][col][ind] = H
        if hl.ship_sunk(opponent['ocean_grid'], col, ind):
            if hl.all_ships_sunk(opponent['ocean_grid']):
                status = WON
            else:
                status = SHIP_SUNK
        else:
            status = HIT
    else:
        status = MISS
        player['targeting_grid'][col][ind] = M
    write_data(player['targeting_grid'], status, move, f_obj)
    if status == WON:
        print(f"{player['name']} Won  !!!!!!!!!!!!!!!!!!!")
        return False
    else:
        print(f"> > > > > > > > > > > > > {status}")
        time.sleep(SLEEP_SECS_BETWEEN_PLAYS)
        return True


def write_data(targeting_grid, status, move, f_obj):
    # move is added to previous line so, it will serve as target variable
    if move != None:
        f_obj.write(f",{move}\n")
    f_obj.write(f"{','.join(targeting_grid.to_numpy().flatten().astype(str))}, {status}")


if __name__ == '__main__':
    print("Battleship Game Started.")
    c_time = datetime.datetime.now().ctime()
    player = player_a
    player['get_input'] = real_user
    opponent = player_b
    opponent['get_input'] = RandomPlayer(opponent).input
    player_filename = f"{player['name']}-moves-status-{c_time}.csv"
    opponent_filename = f"{opponent['name']}-moves-status-{c_time}.csv"
    with open(player_filename, 'w') as player_f, \
            open(opponent_filename, 'w') as opponent_f:
        write_data(player['targeting_grid'], 'N/A', None, player_f)
        write_data(opponent['targeting_grid'], 'N/A', None, opponent_f)
        while play(player, opponent, player_f):
            player, opponent = opponent, player
            player_f, opponent_f = opponent_f, player_f
    print(f"Thanks for defending PicnicHealth")
