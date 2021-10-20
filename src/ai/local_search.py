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
            for cols in MinimaxGroup3.find_valid_col(state):
                for shape in arrShape:
                    placement = place(state, n_player, shape, cols)
                    tupVar = MinimaxGroup3.objective_function(state.board)
                    nodeValue = tupVar[0]
                    v = max(v, nodeValue)

                    if(nodeValue > v):
                        choosenCol = cols
                        choosenShape = shape
            return v, choosenCol, choosenShape

        else:
            v = INFINITY
            for cols in MinimaxGroup3.find_valid_col(state):
                for shape in arrShape:
                    placement = place(state, n_player, shape, cols)
                    tupVar = MinimaxGroup3.objective_function(state.board)
                    nodeValue = tupVar[0]
                    v = min(v, nodeValue)

                    if(nodeValue < v):
                        choosenCol = cols
                        choosenShape = shape
            return v, choosenCol, choosenShape
