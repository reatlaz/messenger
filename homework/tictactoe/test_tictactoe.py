<<<<<<< HEAD
"Unit test module for TicTacToe game class"
=======
>>>>>>> e7383b6 (added Tictactoe and unit tests)
import unittest
import tictactoe

class TestInputValidation(unittest.TestCase):
<<<<<<< HEAD
    "Unit test class for TicTacToe game class"

    def test_input(self):
        "Tests for user input handling"
=======

    def test_input(self):
>>>>>>> e7383b6 (added Tictactoe and unit tests)
        tictac = tictactoe.TicTacToe()
        self.assertTrue(tictac.validate_input('1 2'))
        self.assertTrue(tictac.validate_input('2 3'))

        self.assertFalse(tictac.validate_input('22 55'))
        self.assertFalse(tictac.validate_input('4 2'))
        self.assertFalse(tictac.validate_input('1 5 6 2'))
        self.assertFalse(tictac.validate_input([2, 1]))
        self.assertFalse(tictac.validate_input('0, 1'))
        self.assertFalse(tictac.validate_input('2'))
        self.assertFalse(tictac.validate_input([1, 2, 3]))
        self.assertFalse(tictac.validate_input([55, ]))
        self.assertFalse(tictac.validate_input('he he'))

    def test_game(self):
<<<<<<< HEAD
        "Tests for winner determination"
        tictac = tictactoe.TicTacToe(['X', 'O', ' ', 'X', 'O', ' ', ' ', 'O', 'X'], player='O')
        self.assertEqual(tictac.check_winner(), 'O')

        tictac = tictactoe.TicTacToe(['X', ' ', 'O', 'O', 'X', ' ', 'X', 'O', 'X'], player='X')
        self.assertEqual(tictac.check_winner(), 'X')

        tictac = tictactoe.TicTacToe(['X', ' ', 'X', 'X', 'O', 'X', 'O', 'O', 'O'], player='O')
        self.assertEqual(tictac.check_winner(), 'O')

        tictac = tictactoe.TicTacToe(['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X'],
         player='X', count={'X': 5, 'O': 4})
        self.assertEqual(tictac.check_winner(), 'Draw')

if __name__ == '__main__':
    unittest.main()
=======
        tictac = tictactoe.TicTacToe(['X', 'O', ' ', 'X', 'O', ' ', ' ', 'O', 'X'], 'O')
        self.assertEqual(tictac.check_winner(), 'O')

        tictac = tictactoe.TicTacToe(['X', ' ', 'O', 'O', 'X', ' ', 'X', 'O', 'X'], 'X')
        self.assertEqual(tictac.check_winner(), 'X')

        tictac = tictactoe.TicTacToe(['X', ' ', 'X', 'X', 'O', 'X', 'O', 'O', 'O'], 'O')
        self.assertEqual(tictac.check_winner(), 'O')

        tictac = tictactoe.TicTacToe(['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X'], 'X', {'X': 5, 'O': 4})
        self.assertEqual(tictac.check_winner(), 'Draw')
        

if __name__ == '__main__':
    unittest.main()
>>>>>>> e7383b6 (added Tictactoe and unit tests)
