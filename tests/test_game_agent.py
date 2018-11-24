"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
from game_agent import AlphaBetaPlayer


from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

        

    def test_example(self):
        # TODO: All methods must start with "test_"
        MinMaxPlayer1=AlphaBetaPlayer()
        move=MinMaxPlayer1.get_move(self.game, 2000)
        print(move)


if __name__ == '__main__':
    unittest.main()
