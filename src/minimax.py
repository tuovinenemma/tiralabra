import math
import random 
from board import Game

class Minimax:

    def __init__(self):
        self.game = Game()

    def is_win(self, board, piece):
        """
        Checks if the specified piece has won the game
        :param piece: piece to check (1 or 2)
        :return: True if the piece has won, False otherwise
        """
        # Horizontal
        for col in range(self.game.COLS - 3):
            for row in range(self.game.ROWS):
                if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                    return True

        # Vertical
        for col in range(self.game.COLS):
            for row in range(self.game.ROWS - 3):
                if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                    return True

        # pos diagonal
        for col in range(self.game.COLS - 3):
            for row in range(self.game.ROWS - 3):
                if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                    return True


        # neg diagonal
        for col in range(self.game.COLS - 3):
            for row in range(3, self.game.ROWS):
                if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece and board[row - 3][col + 3] == piece:
                    return True
                
    def rate_possible_move(self, possible_move, piece):
        score = 0
        self.opponent = 1
        if piece == 1:
            self.opponent = 2
        if possible_move.count(piece) == 4:
            score += 100
        elif possible_move.count(piece) == 3 and possible_move.count(self.game.empty) == 1:
            score += 5
        elif possible_move.count(piece) == 2 and possible_move.count(self.game.empty) == 2:
            score += 2
        if possible_move.count(self.opponent) == 3 and possible_move.count(self.game.empty) == 1:
            score -= 5
        
        return score

    def score(self, board, piece):
        score = 0

        # points for center
        center = [int(i) for i in list(board[:,3])]
        count = center.count(piece)
        score += count * 3
        # hor
        for row in range(self.game.ROWS):
            r_array = [int(i) for i in list(board[row, :])]
            for col in range(self.game.COLS -3):
                possible_move = r_array[col:col+4]
                score += self.rate_possible_move(possible_move, piece)

        #ver
        for col in range(self.game.COLS):
            c_array = [int(i) for i in list(board[:,col])]
            for row in range(self.game.ROWS-3):
                possible_move = c_array[row:row+4]
                score += self.rate_possible_move(possible_move, piece)

        #diag
        for row in range(self.game.ROWS-3):
            for col in range(self.game.COLS-3):
                possible_move = [board[row+i][col+i] for i in range(4)]
                score += self.rate_possible_move(possible_move, piece)

        for row in range(self.game.ROWS-3):
            for col in range(self.game.COLS-3):
                possible_move = [board[row+3-i][col+i] for i in range(4)]
                score += self.rate_possible_move(possible_move, piece)

        return score

    def valid_location(self, board):
        valid_locations = []
        for col in range(self.game.COLS):
            if self.game.is_valid_col(board, col):
                valid_locations.append(col)
        return valid_locations

    def best_move(self, board, piece):
        valid_locations = self.valid_location(board)
        best_score = -10000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = self.game.get_empty_row(board, col)
            temp_board = board.copy()
            self.game.drop_piece(temp_board, row, col, piece)
            score = self.score(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col
    def is_terminal(self, board):
        return self.is_win(board, 1) or self.is_win(board, 2) or len(self.valid_location(board)) == 0
    
    def minimax(self, board, depth, maxPlayer):
        valid_locations = self.valid_location(board)
        terminal = self.is_terminal(board)
        if depth == 0 or terminal:
            if terminal:
                if self.is_win(board, 2):
                    return (None, 100000000000000)
                elif self.is_win(board, 1):
                    return (None, -10000000000000)
                else:
                    return (None, 0)
            else:
                return (None, self.score(board, 2))
            
        if maxPlayer:
            value = -math.inf
            column = random.choice([i for i in range(self.game.COLS) if self.game.is_valid_col(board, i)])
            for col in valid_locations:
                row = self.game.get_empty_row(board, col)
                copy_board = board.copy()
                self.game.drop_piece(copy_board, row, col, 2)
                new_score = self.minimax(copy_board, depth-1, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
            return column, value
            
        else:
            value = math.inf
            column = random.choice([i for i in range(self.game.COLS) if self.game.is_valid_col(board, i)])
            for col in valid_locations:
                row = self.game.get_empty_row(board, col)
                copy_board = board.copy()
                self.game.drop_piece(copy_board, row, col, 1)
                new_score = self.minimax(copy_board, depth-1, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
            return column, value