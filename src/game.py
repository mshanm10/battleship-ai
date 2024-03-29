import pandas as pd
import numpy as np
import helper as hl
import datetime
import itertools
import random
import time
from joblib import load

tg_grid = pd.DataFrame(np.zeros((5, 5), dtype=int), columns=['A', 'B', 'C', 'D', 'E'], index=[1, 2, 3, 4, 5])
B = 0  # blank
S = 2  # ship
H = 1  # hit
M = -1  # miss

SLEEP_SECS_BETWEEN_PLAYS = 0


def as_grid(nparray):
    return pd.DataFrame(nparray, columns=['A', 'B', 'C', 'D', 'E'], index=[1, 2, 3, 4, 5])

'''
Ocean grid is choosen randomly one for each player.
'''
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


class XGBoostAIPlayer(object):

    def __init__(self, player, tg_grid):
        self.col_clf = load('clf-col-xgboost-Sun Oct 20 23:47:50 2019.joblib')
        self.row_clf = load('clf-row-xgboost-Sun Oct 20 23:48:55 2019.joblib')
        self.prev_attack_dum = None
        self.prev_attack('a1')
        self.update_result(tg_grid, MISS)

    def prev_attack(self, attack):
        attack = attack.lower()
        col_dum = self.dummies(attack[0], ['a', 'b', 'c', 'd', 'e'],
                               ['prev_attack_col_a', 'prev_attack_col_b', 'prev_attack_col_c', 'prev_attack_col_d',
                                'prev_attack_col_e'])
        row_dum = self.dummies(attack[1], ['1', '2', '3', '4', '5'],
                               ['prev_attack_row_1', 'prev_attack_row_2', 'prev_attack_row_3', 'prev_attack_row_4',
                                'prev_attack_row_5'])
        self.prev_attack_dum = pd.concat([col_dum, row_dum], axis=1)

    def input(self):
        print(f"{player['name']}'s attack (eg:A1)): XGBoost AI player playing...(please wait)")
        time.sleep(SLEEP_SECS_BETWEEN_PLAYS)
        col_pred = self.col_clf.predict(self.X_col)[0]
        dum_df = self.dummies(col_pred, ['a', 'b', 'c', 'd', 'e'],
                              ['attack_col_a', 'attack_col_b', 'attack_col_c', 'attack_col_d', 'attack_col_e'])
        X_row = pd.concat([self.X_col, dum_df], axis=1)
        row_pred = self.row_clf.predict(X_row)[0]
        move = f'{col_pred}{row_pred}'.upper()
        self.prev_attack(move)
        return move

    def dummies(self, curr_val, values, columns):
        col_values = np.array(values)
        col_names = columns
        return pd.DataFrame(np.array([1 if c else 0 for c in col_values == curr_val]).reshape(1, -1), columns=col_names)

    def update_result(self, tg_grid, status):
        cols = [f'cor_{i}' for i in range(25)]
        df = pd.DataFrame(tg_grid.to_numpy().flatten().reshape((1, -1)), columns=cols)
        sts_df = self.dummies(status, [HIT, SHIP_SUNK, MISS],
                              ['status_hit', 'status_miss', 'status_shipsunk'])
        self.X_col = pd.concat([df, sts_df, self.prev_attack_dum], axis=1)


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
    move = ''
    while move == '':
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
        if 'update_result' in player:
            player['update_result'](player['targeting_grid'], status)
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
    # player['get_input'] = real_user  # Uncomment this to play manually
    # comment below 3 lines to play manually
    xgboost_ai_player = XGBoostAIPlayer(player, player['targeting_grid'])
    player['get_input'] = xgboost_ai_player.input
    player['update_result'] = xgboost_ai_player.update_result

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
