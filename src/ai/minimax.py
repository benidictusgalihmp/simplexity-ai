import random
from time import time

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return best_movement

import random
from copy import deepcopy
from time import time

from src.utility import *
from src.model import State
from src.model import Board
from src.model import Config
from src.constant import ColorConstant
from src.constant import ShapeConstant
from src.constant import GameConstant

from typing import Tuple, List


class Minimax2:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return best_movement

    def calculate_piece_score(self, board: Board, row: int, col: int, player_shape: str, player_color: str):
        if player_color == ColorConstant.RED and player_shape == ShapeConstant.CIRCLE:
            if board.board[row][col].color == ColorConstant.RED and board.board[row][col].shape == ShapeConstant.CIRCLE:
                return 3
            elif board.board[row][col].color == ColorConstant.BLUE and board.board[row][col].shape == ShapeConstant.CIRCLE:
                return 2
            elif board.board[row][col].color == ColorConstant.RED and board.board[row][col].shape == ShapeConstant.CROSS:
                return 1
            elif board.board[row][col].color == ColorConstant.BLUE and board.board[row][col].shape == ShapeConstant.CROSS:
                return -1
        elif player_color == ColorConstant.BLUE and player_shape == ShapeConstant.CIRCLE:
            if board.board[row][col].color == ColorConstant.BLUE and board.board[row][col].shape == ShapeConstant.CIRCLE:
                return 3
            elif board.board[row][col].color == ColorConstant.RED and board.board[row][col].shape == ShapeConstant.CIRCLE:
                return 2
            elif board.board[row][col].color == ColorConstant.BLUE and board.board[row][col].shape == ShapeConstant.CROSS:
                return 1
            elif board.board[row][col].color == ColorConstant.RED and board.board[row][col].shape == ShapeConstant.CROSS:
                return -1
        elif player_color == ColorConstant.RED and player_shape == ShapeConstant.CROSS:
            if board.board[row][col].color == ColorConstant.RED and board.board[row][col].shape == ShapeConstant.CROSS:
                return 3
            elif board.board[row][col].color == ColorConstant.BLUE and board.board[row][col].shape == ShapeConstant.CROSS:
                return 2
            elif board.board[row][col].color == ColorConstant.RED and board.board[row][col].shape == ShapeConstant.CIRCLE:
                return 1
            elif board.board[row][col].color == ColorConstant.BLUE and board.board[row][col].shape == ShapeConstant.CIRCLE:
                return -1
        elif player_color == ColorConstant.BLUE and player_shape == ShapeConstant.CROSS:
            if board.board[row][col].color == ColorConstant.BLUE and board.board[row][col].shape == ShapeConstant.CROSS:
                return 3
            elif board.board[row][col].color == ColorConstant.RED and board.board[row][col].shape == ShapeConstant.CROSS:
                return 2
            elif board.board[row][col].color == ColorConstant.BLUE and board.board[row][col].shape == ShapeConstant.CIRCLE:
                return 1
            elif board.board[row][col].color == ColorConstant.RED and board.board[row][col].shape == ShapeConstant.CIRCLE:
                return -1

        return 0

    def calculate_horizontal_score(self, board: Board, config: Config):
        horizontal_score = 0
        for i in range(config.row):
            for j in range(config.col - 3):
                count_piece = 0
                player1_temp_score = 0
                player2_temp_score = 0
                is_player1_can_win = True
                is_player2_can_win = True
                line_pieces = []
                for k in range(4):
                    if i + 1 < config.row and board.board[i + 1][j + k].shape == ShapeConstant.BLANK:
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

                    if self.calculate_piece_score(board, i, j + k, GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR) == -1:
                        player1_temp_score = 0
                        is_player1_can_win = False

                    if self.calculate_piece_score(board, i, j + k, GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR) == -1:
                        player2_temp_score = 0
                        is_player2_can_win = False

                    if not(is_player1_can_win) and not(is_player2_can_win):
                        break

                    if (board.board[i][j + k].shape != ShapeConstant.BLANK):
                        count_piece += 1

                    if is_player1_can_win:
                        player1_temp_score += self.calculate_piece_score(board, i, j + k, GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR)

                    if is_player2_can_win:
                        player2_temp_score += self.calculate_piece_score(board, i, j + k, GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR)

                if count_piece == 4:
                    horizontal_score += player1_temp_score * 999 - player2_temp_score * 999
                else:
                    horizontal_score += player1_temp_score * count_piece - player2_temp_score * count_piece
                
        return horizontal_score

    def calculate_vertical_score(self, board: Board, config: Config):
        vertical_score = 0
        for i in range(3, config.row):
            for j in range(config.col):
                count_piece = 0
                player1_temp_score = 0
                player2_temp_score = 0
                is_player1_can_win = True
                is_player2_can_win = True
                line_pieces = []
                for k in range(4):
                    if i + 1 < config.row and board.board[i + 1 - k][j].shape == ShapeConstant.BLANK:
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

                    if self.calculate_piece_score(board, i - k, j, GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR) == -1:
                        player1_temp_score = 0
                        is_player1_can_win = False

                    if self.calculate_piece_score(board, i - k, j, GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR) == -1:
                        player2_temp_score = 0
                        is_player2_can_win = False

                    if not(is_player1_can_win) and not(is_player2_can_win):
                        break

                    if (board.board[i - k][j].shape != ShapeConstant.BLANK):
                        count_piece += 1

                    if is_player1_can_win:
                        player1_temp_score += self.calculate_piece_score(board, i - k, j, GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR)

                    if is_player2_can_win:
                        player2_temp_score += self.calculate_piece_score(board, i - k, j, GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR)

                if count_piece == 4:
                    vertical_score += player1_temp_score * 999 - player2_temp_score * 999
                else:
                    vertical_score += player1_temp_score * count_piece - player2_temp_score * count_piece

        return vertical_score

    def calculate_diagonal_right_score(self, board: Board, config: Config):
        diagonal_right_score = 0
        for i in range(3, config.row):
            for j in range(config.col - 3):
                count_piece = 0
                player1_temp_score = 0
                player2_temp_score = 0
                is_player1_can_win = True
                is_player2_can_win = True
                line_pieces = []
                for k in range(4):
                    if i + 1 < config.row and board.board[i + 1 - k][j + k].shape == ShapeConstant.BLANK:
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

                    if self.calculate_piece_score(board, i - k, j + k, GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR) == -1:
                        player1_temp_score = 0
                        is_player1_can_win = False

                    if self.calculate_piece_score(board, i - k, j + k, GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR) == -1:
                        player2_temp_score = 0
                        is_player2_can_win = False

                    if not(is_player1_can_win) and not(is_player2_can_win):
                        break

                    if (board.board[i - k][j + k].shape != ShapeConstant.BLANK):
                        count_piece += 1

                    if is_player1_can_win:
                        player1_temp_score += self.calculate_piece_score(board, i - k, j + k, GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR)

                    if is_player2_can_win:
                        player2_temp_score += self.calculate_piece_score(board, i - k, j + k, GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR)

                if count_piece == 4:
                    diagonal_right_score += player1_temp_score * 999 - player2_temp_score * 999
                else:
                    diagonal_right_score += player1_temp_score * count_piece - player2_temp_score * count_piece

        return diagonal_right_score

    def calculate_diagonal_left_score(self, board: Board, config: Config):
        diagonal_left_score = 0
        for i in range(3, config.row):
            for j in range(3, config.col):
                count_piece = 0
                player1_temp_score = 0
                player2_temp_score = 0
                is_player1_can_win = True
                is_player2_can_win = True
                line_pieces = []
                for k in range(4):
                    if i + 1 < config.row and board.board[i + 1 - k][j - k].shape == ShapeConstant.BLANK:
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

                    if self.calculate_piece_score(board, i - k, j - k, GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR) == -1:
                        player1_temp_score = 0
                        is_player1_can_win = False

                    if self.calculate_piece_score(board, i - k, j - k, GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR) == -1:
                        player2_temp_score = 0
                        is_player2_can_win = False

                    if not(is_player1_can_win) and not(is_player2_can_win):
                        break

                    if (board.board[i - k][j - k].shape != ShapeConstant.BLANK):
                        count_piece += 1

                    if is_player1_can_win:
                        player1_temp_score += self.calculate_piece_score(board, i - k, j - k, GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR)

                    if is_player2_can_win:
                        player2_temp_score += self.calculate_piece_score(board, i - k, j - k, GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR)

                if count_piece == 4:
                    diagonal_left_score += player1_temp_score * 999 - player2_temp_score * 999
                else:
                    diagonal_left_score += player1_temp_score * count_piece - player2_temp_score * count_piece

        return diagonal_left_score

    def objective_function(self, board: Board, config: Config):
        print("horizontal score: " + str(self.calculate_horizontal_score(board, config)))
        print("vertical score: " + str(self.calculate_vertical_score(board, config)))
        print("diagonal right score: " + str(self.calculate_diagonal_right_score(board, config)))
        print("diagonal left score: " + str(self.calculate_diagonal_left_score(board, config)))
        return self.calculate_horizontal_score(board, config) + self.calculate_vertical_score(board, config) + self.calculate_diagonal_right_score(board, config) + self.calculate_diagonal_left_score(board, config)