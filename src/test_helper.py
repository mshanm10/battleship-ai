import unittest
import helper as h
import pandas as pd
from game import S, H


class TestHelper(unittest.TestCase):
    def test_ship_sunk(self):
        grid = pd.DataFrame([[0, 0, 0, 0, H],
                             [0, 0, 0, 0, H],
                             [S, S, S, 0, H],
                             [0, 0, 0, 0, 0],
                             [0, 0, S, S, H]], columns=['A', 'B', 'C', 'D', 'E'], index=[1, 2, 3, 4, 5])
        self.assertFalse(h.ship_sunk(grid, 'B', 3))
        self.assertTrue(h.ship_sunk(grid, 'E', 1))
        self.assertFalse(h.ship_sunk(grid, 'C', 3))

    def test_all_ships_sunk(self):
        grid = pd.DataFrame([[0, 0, 0, 0, H],
                             [0, 0, 0, 0, H],
                             [S, S, S, 0, H],
                             [0, 0, 0, 0, 0],
                             [0, 0, S, S, H]], columns=['A', 'B', 'C', 'D', 'E'], index=[1, 2, 3, 4, 5])
        self.assertFalse(h.all_ships_sunk(grid))
        grid = pd.DataFrame([[0, 0, 0, 0, H],
                             [0, 0, 0, 0, H],
                             [H, H, H, 0, H],
                             [0, 0, 0, 0, 0],
                             [0, 0, H, H, H]], columns=['A', 'B', 'C', 'D', 'E'], index=[1, 2, 3, 4, 5])
        self.assertTrue(h.all_ships_sunk(grid))


if __name__ == '__main__':
    unittest.main()
