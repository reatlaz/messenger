"""
Home-task №1: Making a TicTacToe game class
"""


class TicTacToe:
    """A functioning class representing a game of TicTacToe"""
    grid = []
    count = {}
    player = ''

    def __init__(self, grid=None, player='X', count=None):
        if grid is None:
            grid = [' '] * 9
        if count is None:
            count = {}
        self.grid = grid
        self.player = player
        self.count = count

    def show_board(self):
        """A method that print the grid to terminal"""

        print('---------')
        for i in range(3):
            print('| ', end='')
            for j in range(3):
                print(self.grid[j + 3 * i] + ' ', end='')
            print('|')
        print('---------')

    def validate_input(self, inp):
        """A method that processes each move made by players"""

        if not isinstance(inp, str):
            print('Enter two numbers divided by one space')
            return False

        coords = inp.split()
        if len(coords) != 2 or not coords[0].isdigit() or not coords[1].isdigit():
            print('Enter two whole positive numbers divided by one space')
            return False

        x_column = int(coords[0]) - 1
        y_line = int(coords[1]) - 1

        if y_line > 2 or y_line < 0 or x_column > 2 or x_column < 0:
            print('Coordinates should be from 1 to 3!')
            return False

        if self.grid[x_column + y_line * 3] == 'X' or self.grid[x_column + y_line * 3] == 'O':
            print('This cell is occupied! Choose another one!')
            return False

        return True

    def start_game(self):
        """A method that starts the actual game"""
        self.grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.count = {'X': 0, 'O': 0}
        while True:
            self.show_board()
            # validating input
            play = input('Enter the coordinates:')
            while self.validate_input(play) is False:
                play = input('Enter the coords:')
            # pulling coords out of input
            coords = play.split()
            y_line = int(coords[0]) - 1
            x_column = int(coords[1]) - 1
            # making the play
            self.grid[x_column * 3 + y_line] = self.player
            self.count[self.player] += 1
            # checking if the game is finished
            if self.check_winner() != 0:
                break
            # switching player
            if self.player == 'X':
                self.player = 'O'
            else:
                self.player = 'X'

    def check_winner(self):
        """A method that returns game state: 0 if game is in progress, X or O if a player has won"""
        winner = 0
        if self.grid[0] == self.grid[4] == self.grid[8] != ' ':
            winner = self.grid[0]
        elif self.grid[2] == self.grid[4] == self.grid[6] != ' ':
            winner = self.grid[2]
        else:
            for i in range(3):
                if (self.grid[i * 3] == self.grid[i * 3 + 1] == self.grid[i * 3 + 2] != ' '
                        or self.grid[i] == self.grid[i + 3] == self.grid[i + 6] != ' '):
                    if winner == 0:
                        winner = self.player

        if winner == 0 and self.count['X'] + self.count['O'] == 9:
            winner = 'Draw'
            self.show_board()
            print(winner)
            return winner

        if winner != 0:
            self.show_board()
            print(winner, 'wins')
            return winner

        return 0


if __name__ == '__main__':
    game = TicTacToe()
    game.start_game()
