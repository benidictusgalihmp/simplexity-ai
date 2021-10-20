import random
from time import time

from src.constant import ShapeConstant
from src.model import State
from src.constant import ColorConstant, ShapeConstant, GameConstant
from src.utility import *

from typing import Tuple, List

from src.ai.minimax import MinimaxGroup3

INFINITY = 99999999
arrShape = [ShapeConstant.CROSS, ShapeConstant.CIRCLE]

class LocalSearchGroup3:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        choosen_col, choosen_shape = self.localSearch(state, n_player)

        best_movement = (choosen_col, choosen_shape) #local search algorithm

        return best_movement

    '''


    @params :
    @return :
    '''
    def localSearch(self, state, n_player):
        choosenCol = 0
        choosenShape = ShapeConstant.CIRCLE

        if(n_player):
            v = -INFINITY
            for cols in self.find_valid_col(state):
                for shape in arrShape:
                    placement = place(state, n_player, shape, cols)
                    tupVar = self.objective_function(state.board)
                    nodeValue = tupVar[0]
                    v = max(v, nodeValue)

                    if(nodeValue > v):
                        choosenCol = cols
                        choosenShape = shape
            return v, choosenCol, choosenShape

        else:
            v = INFINITY
            for cols in self.find_valid_col(state):
                for shape in arrShape:
                    placement = place(state, n_player, shape, cols)
                    tupVar = self.objective_function(state.board)
                    nodeValue = tupVar[0]
                    v = min(v, nodeValue)

                    if(nodeValue < v):
                        choosenCol = cols
                        choosenShape = shape
            return v, choosenCol, choosenShape

    '''
    Finding all valid columns index in State.board
    Columns is valid if ShapeConstant.BLANK in array id column
    @params : State
    @return : integer array
    '''
    def find_valid_col(self, state: State):
        validCol = []
        arrcol = []
        blankObj = Piece(ShapeConstant.BLANK,ColorConstant.BLACK)

        for iCol in range(state.board.col):
            piece = state.board.board[0][iCol]    # get array elemen in column[iCol]

            if(piece == blankObj):             # BLANK shape in column[iCol]
                validCol.append(iCol)           # add iCol into array validCol
        
        return validCol
    
    def calculate_piece_score(self, piece: Piece, player_shape: str, player_color: str):
        if player_color == ColorConstant.RED and player_shape == ShapeConstant.CIRCLE:
            if piece.color == ColorConstant.RED and piece.shape == ShapeConstant.CIRCLE:
                return 3
            elif piece.color == ColorConstant.BLUE and piece.shape == ShapeConstant.CIRCLE:
                return 2
            elif piece.color == ColorConstant.RED and piece.shape == ShapeConstant.CROSS:
                return 1
            elif piece.color == ColorConstant.BLUE and piece.shape == ShapeConstant.CROSS:
                return -1
        elif player_color == ColorConstant.BLUE and player_shape == ShapeConstant.CIRCLE:
            if piece.color == ColorConstant.BLUE and piece.shape == ShapeConstant.CIRCLE:
                return 3
            elif piece.color == ColorConstant.RED and piece.shape == ShapeConstant.CIRCLE:
                return 2
            elif piece.color == ColorConstant.BLUE and piece.shape == ShapeConstant.CROSS:
                return 1
            elif piece.color == ColorConstant.RED and piece.shape == ShapeConstant.CROSS:
                return -1
        elif player_color == ColorConstant.RED and player_shape == ShapeConstant.CROSS:
            if piece.color == ColorConstant.RED and piece.shape == ShapeConstant.CROSS:
                return 3
            elif piece.color == ColorConstant.BLUE and piece.shape == ShapeConstant.CROSS:
                return 2
            elif piece.color == ColorConstant.RED and piece.shape == ShapeConstant.CIRCLE:
                return 1
            elif piece.color == ColorConstant.BLUE and piece.shape == ShapeConstant.CIRCLE:
                return -1
        elif player_color == ColorConstant.BLUE and player_shape == ShapeConstant.CROSS:
            if piece.color == ColorConstant.BLUE and piece.shape == ShapeConstant.CROSS:
                return 3
            elif piece.color == ColorConstant.RED and piece.shape == ShapeConstant.CROSS:
                return 2
            elif piece.color == ColorConstant.BLUE and piece.shape == ShapeConstant.CIRCLE:
                return 1
            elif piece.color == ColorConstant.RED and piece.shape == ShapeConstant.CIRCLE:
                return -1

        return 0

    def calculate_horizontal_score(self, board: Board):
        horizontal_score = 0
        for i in range(board.row):
            for j in range(board.col - 3):
                count_piece = 0
                player1_temp_score = 0
                player2_temp_score = 0
                is_player1_can_win = True
                is_player2_can_win = True
                line_pieces = []
                for k in range(4):
                    if i + 1 < board.row and board.board[i + 1][j + k].shape == ShapeConstant.BLANK:
                        break

                    is_exist = False
                    for l in range(len(line_pieces)):
                        if line_pieces[l] == board.board[i][j + k]:
                            is_exist = True
                            break

                    if not(is_exist) and board.board[i][j + k].shape != ShapeConstant.BLANK:
                        line_pieces.append(board.board[i][j + k])

                    if len(line_pieces) >= 3:
                        player1_temp_score = 0
                        player2_temp_score = 0
                        is_player1_can_win = False
                        is_player2_can_win = False

                    if self.calculate_piece_score(board.board[i][j + k], GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR) == -1:
                        player1_temp_score = 0
                        is_player1_can_win = False

                    if self.calculate_piece_score(board.board[i][j + k], GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR) == -1:
                        player2_temp_score = 0
                        is_player2_can_win = False

                    if not(is_player1_can_win) and not(is_player2_can_win):
                        break

                    if (board.board[i][j + k].shape != ShapeConstant.BLANK):
                        count_piece += 1

                    if is_player1_can_win:
                        player1_temp_score += self.calculate_piece_score(board.board[i][j + k], GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR)

                    if is_player2_can_win:
                        player2_temp_score += self.calculate_piece_score(board.board[i][j + k], GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR)

                if count_piece == 4:
                    horizontal_score += player1_temp_score * 999 - player2_temp_score * 999
                else:
                    horizontal_score += player1_temp_score * count_piece - player2_temp_score * count_piece
                
        return horizontal_score

    def calculate_vertical_score(self, board: Board):
        vertical_score = 0
        for i in range(3, board.row):
            for j in range(board.col):
                count_piece = 0
                player1_temp_score = 0
                player2_temp_score = 0
                is_player1_can_win = True
                is_player2_can_win = True
                line_pieces = []
                for k in range(4):
                    if i + 1 < board.row and board.board[i + 1 - k][j].shape == ShapeConstant.BLANK:
                        break

                    is_exist = False
                    for l in range(len(line_pieces)):
                        if line_pieces[l] == board.board[i - k][j]:
                            is_exist = True
                            break

                    if not(is_exist) and board.board[i - k][j].shape != ShapeConstant.BLANK:
                        line_pieces.append(board.board[i - k][j])

                    if len(line_pieces) >= 3:
                        player1_temp_score = 0
                        player2_temp_score = 0
                        is_player1_can_win = False
                        is_player2_can_win = False

                    if self.calculate_piece_score(board.board[i - k][j], GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR) == -1:
                        player1_temp_score = 0
                        is_player1_can_win = False

                    if self.calculate_piece_score(board.board[i - k][j], GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR) == -1:
                        player2_temp_score = 0
                        is_player2_can_win = False

                    if not(is_player1_can_win) and not(is_player2_can_win):
                        break

                    if (board.board[i - k][j].shape != ShapeConstant.BLANK):
                        count_piece += 1

                    if is_player1_can_win:
                        player1_temp_score += self.calculate_piece_score(board.board[i - k][j], GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR)

                    if is_player2_can_win:
                        player2_temp_score += self.calculate_piece_score(board.board[i - k][j], GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR)

                if count_piece == 4:
                    vertical_score += player1_temp_score * 999 - player2_temp_score * 999
                else:
                    vertical_score += player1_temp_score * count_piece - player2_temp_score * count_piece

        return vertical_score

    def calculate_diagonal_right_score(self, board: Board):
        diagonal_right_score = 0
        for i in range(3, board.row):
            for j in range(board.col - 3):
                count_piece = 0
                player1_temp_score = 0
                player2_temp_score = 0
                is_player1_can_win = True
                is_player2_can_win = True
                line_pieces = []
                for k in range(4):
                    if i + 1 < board.row and board.board[i + 1 - k][j + k].shape == ShapeConstant.BLANK:
                        break

                    is_exist = False
                    for l in range(len(line_pieces)):
                        if line_pieces[l] == board.board[i - k][j + k]:
                            is_exist = True
                            break

                    if not(is_exist) and board.board[i - k][j + k].shape != ShapeConstant.BLANK:
                        line_pieces.append(board.board[i - k][j + k])

                    if len(line_pieces) >= 3:
                        player1_temp_score = 0
                        player2_temp_score = 0
                        is_player1_can_win = False
                        is_player2_can_win = False

                    if self.calculate_piece_score(board.board[i - k][j + k], GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR) == -1:
                        player1_temp_score = 0
                        is_player1_can_win = False

                    if self.calculate_piece_score(board.board[i - k][j + k], GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR) == -1:
                        player2_temp_score = 0
                        is_player2_can_win = False

                    if not(is_player1_can_win) and not(is_player2_can_win):
                        break

                    if (board.board[i - k][j + k].shape != ShapeConstant.BLANK):
                        count_piece += 1

                    if is_player1_can_win:
                        player1_temp_score += self.calculate_piece_score(board.board[i - k][j + k], GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR)

                    if is_player2_can_win:
                        player2_temp_score += self.calculate_piece_score(board.board[i - k][j + k], GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR)

                if count_piece == 4:
                    diagonal_right_score += player1_temp_score * 999 - player2_temp_score * 999
                else:
                    diagonal_right_score += player1_temp_score * count_piece - player2_temp_score * count_piece

        return diagonal_right_score

    def calculate_diagonal_left_score(self, board: Board):
        diagonal_left_score = 0
        for i in range(3, board.row):
            for j in range(3, board.col):
                count_piece = 0
                player1_temp_score = 0
                player2_temp_score = 0
                is_player1_can_win = True
                is_player2_can_win = True
                line_pieces = []
                for k in range(4):
                    if i + 1 < board.row and board.board[i + 1 - k][j - k].shape == ShapeConstant.BLANK:
                        break

                    is_exist = False
                    for l in range(len(line_pieces)):
                        if line_pieces[l] == board.board[i - k][j - k]:
                            is_exist = True
                            break

                    if not(is_exist) and board.board[i - k][j - k].shape != ShapeConstant.BLANK:
                        line_pieces.append(board.board[i - k][j - k])

                    if len(line_pieces) >= 3:
                        player1_temp_score = 0
                        player2_temp_score = 0
                        is_player1_can_win = False
                        is_player2_can_win = False

                    if self.calculate_piece_score(board.board[i - k][j - k], GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR) == -1:
                        player1_temp_score = 0
                        is_player1_can_win = False

                    if self.calculate_piece_score(board.board[i - k][j - k], GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR) == -1:
                        player2_temp_score = 0
                        is_player2_can_win = False

                    if not(is_player1_can_win) and not(is_player2_can_win):
                        break

                    if (board.board[i - k][j - k].shape != ShapeConstant.BLANK):
                        count_piece += 1

                    if is_player1_can_win:
                        player1_temp_score += self.calculate_piece_score(board.board[i - k][j - k], GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR)

                    if is_player2_can_win:
                        player2_temp_score += self.calculate_piece_score(board.board[i - k][j - k], GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR)

                if count_piece == 4:
                    diagonal_left_score += player1_temp_score * 999 - player2_temp_score * 999
                else:
                    diagonal_left_score += player1_temp_score * count_piece - player2_temp_score * count_piece

        return diagonal_left_score

    def objective_function(self, board: Board):
        return self.calculate_horizontal_score(board) + self.calculate_vertical_score(board) + self.calculate_diagonal_right_score(board) + self.calculate_diagonal_left_score(board)
    