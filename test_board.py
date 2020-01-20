import unittest

from generateMap import Board
from room import Room
from exceptions import *
from settings import *
from parameterized import parameterized
import copy

minBoardSize = MIN_BOARD_HEIGHT
modestBoardSize = minBoardSize * 4

generalTestBoardParams = (modestBoardSize, modestBoardSize - 3)
generalTestBoardX, generalTestBoardY = generalTestBoardParams
generalRoomSize = (5,5)

# array of entries of form [String:name, Int:x, Int:y, RoomOutsideBoard or None:exception]
RoomPlacements = [
		["X is too small", 0, 1, RoomOutsideBoard],
		["Y is too small", 1, 0, RoomOutsideBoard],
		["X and Y are too small", 0, 0, RoomOutsideBoard],
		["X and Y are just within bounds on the top left", 1, 1, None],
		["Y is just within bounds on the bottom left", 1, generalTestBoardY - 6, None],
		["X is just within bounds on the top right", generalTestBoardX - 6, 1, None],
		["X and Y are just within bounds on the bottom right", generalTestBoardX-6, generalTestBoardY-6, None],
		["Y is just outside bounds on the bottom left", 1, generalTestBoardY - 5, RoomOutsideBoard],
		["X is just outside bounds on the top right", generalTestBoardX - 5, 1, RoomOutsideBoard],
		["X and Y are just outside bounds on the bottom right", generalTestBoardX - 5, generalTestBoardY - 5, RoomOutsideBoard]
]

boardState1 = [['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '&', '*', '*', '*', '&', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`']]
boardState2 = [['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '&', '*', '*', '*', '&', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`']]
boardState3 = [['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '&', '*', '*', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '&', '*', '*', '*', '&', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '&', '*', '*', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`']]
boardState4 = [['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '&', '*', '*', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '&', '*', '*', '*', '&', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '&', '*', '*', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`']]


boardState_connect_1 = [['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '&', '*', '*', '*', '-', '-', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '-', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '-', '-', '-', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '-', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '&', '*', '*', '*', '&', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`']]
boardState_connect_2 = [['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`'], ['`', '&', '*', '*', '*', '-', '-', '-', '-', '-', '-', '*', '*', '*', '&', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`']]
boardState_connect_3 = [['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '&', '*', '*', '*', '-', '-', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '-', '-', '-', '-', '-', '-', '-', '-', '-', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '&', '*', '*', '`', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '&', '*', '*', '*', '-', '-', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`']]

boardState_connect_complex_1 = [['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '&', '*', '*', '*', '-', '-', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '-', '*', '*', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '-', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '-', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '-', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '-', '*', '*', '`', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '&', '*', '*', '*', '-', '-', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`']]
boardState_connect_complex_2 = [['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '&', '*', '*', '*', '-', '-', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '-', '*', '*', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '-', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '-', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '-', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '*', '*', '&', '*', '*', '`', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '*', '*', '*', '*', '*', '`', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '-', '-', '-', '-', '*', '*', '*', '-', '-', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`']]
boardState_connect_complex_3 = [['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '&', '*', '*', '*', '-', '-', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '-', '*', '*', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '-', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '-', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '-', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '-', '*', '*', '`', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '&', '*', '*', '*', '-', '-', '-', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`']]


'''
#fragile way of generating
["X and Y are just within bounds on the bottom right", generalTestBoardX-6, generalTestBoardY-6, boardState1],
["Y is just outside bounds on the bottom left", 1, generalTestBoardY - 5, boardState2],
["X is just outside bounds on the top right", generalTestBoardX - 5, 1, boardState3],
["X and Y are just outside bounds on the bottom right", generalTestBoardX - 5, generalTestBoardY - 5, boardState4]


roomPlacementsNoExceptions = [r for r in RoomPlacements if r[-1] is None]
bs = [boardState1, boardState2, boardState3, boardState4]

for testcase, boardState in list(zip(roomPlacementsNoExceptions, bs)):
	tc = testcase + [boardState]
'''




# used to test if points are reported as inside or outside the board
# will be an array of entries of form
# [ String:name, 2-entry-tuple:point, PointOutsideBoard or None:exception ]
pointTests = []

# middle of board, should be in range
tempX, tempY = generalTestBoardParams
tempX, tempY = tempX // 2, tempY // 2
pointTests.append(["middle of board", (tempX, tempY), None])

# just inside board, should be in range
tempX, tempY = generalTestBoardParams
tempX, tempY = tempX -2, tempY -2
pointTests.append(["just inside of board", (tempX, tempY), None])

# on corner, should be in range
tempX, tempY = generalTestBoardParams
tempX, tempY = tempX -1, tempY -1
pointTests.append(["on corner of board", (tempX, tempY), None])

# just outside board, should NOT be in range
tempX, tempY = generalTestBoardParams
tempX, tempY = tempX-1, tempY
pointTests.append(["just outside of board Y", (tempX, tempY), PointOutsideBoard])

# just outside board, should NOT be in range
tempX, tempY = generalTestBoardParams
tempX, tempY = tempX, tempY -1
pointTests.append(["just outside of board X", (tempX, tempY), PointOutsideBoard])

# very outside board, should NOT be in range
tempX, tempY = generalTestBoardParams
tempX, tempY = tempX * 4, tempY * 4
pointTests.append(["very outside of board X", (tempX, tempY), PointOutsideBoard])


parentsAndPaths = [
	[{(8, 5): None, (7, 5): (8, 5), (6, 5): (7, 5), (5, 5): (6, 5), (6, 4): (6, 5), (4, 5): (5, 5), (5, 4): (5, 5), (3, 5): (4, 5), (4, 4): (4, 5), (4, 6): (4, 5), (4, 7): (4, 6)}, [(8, 5), (7, 5), (6, 5), (5, 5), (4, 5), (4, 6), (4, 7)]],
	[{(3, 2): None, (4, 2): (3, 2), (5, 2): (4, 2), (6, 2): (5, 2), (5, 1): (5, 2), (5, 3): (5, 2), (5, 5): (5, 4), (4, 5): (5, 5), (6, 5): (5, 5), (7, 5): (6, 5), (8, 5): (7, 5), (4, 6): (4, 5), (4, 7): (4, 6), (5, 4): (5, 3)}, [(3, 2), (4, 2), (5, 2), (5, 3), (5, 4), (5, 5), (4, 5), (4, 6), (4, 7)]]
]


class TestRoomCreation(unittest.TestCase):
	@parameterized.expand([
		["small width", (minBoardSize, modestBoardSize)],
		["small height", (modestBoardSize, minBoardSize)],
		["both small", (minBoardSize, minBoardSize)],
		["modest sized", (modestBoardSize, modestBoardSize)]
	])
	def test_correct_board_creation(self, name, boardParams):
		b = Board(*boardParams)
		(width, height) = boardParams
		self.assertEqual(height, b.height)
		self.assertEqual(width, b.width)

		# all chars are set to "blocked" at first
		self.assertTrue(all(
			b._board[y][x] == charSet["blocked"]
			for y in range(b.height)
			for x in range(b.width)
		))

	def test_board_change_tile(self):
		b = Board(*generalTestBoardParams)
		point = (0, 0)
		charToChangeTo = charSet["start"]  # initial board is filled with 'blocked'

		# grab initial state of the char
		initialState = b._get_tile(point)

		# change state of position on board
		b._change_tile(point, charToChangeTo)

		# check the change took
		changedState = b._get_tile(point)

		self.assertNotEqual(initialState, changedState)
		self.assertEqual(changedState, charToChangeTo)

	@parameterized.expand(pointTests)
	def test_board_change_tile_range(self, name, point, exception):
		b = Board(*generalTestBoardParams)
		charToChangeTo = charSet["start"]  # initial board is filled with 'blocked'

		if exception is None:
			# change state of position on board
			b._change_tile(point, charToChangeTo)
		else:
			# equiv to "b._change_tile(point, charToChangeTo)"
			self.assertRaises(exception, b._change_tile, point, charToChangeTo)

	@parameterized.expand(pointTests)
	def test_board_get_tile_range(self, name, point, exception):
		b = Board(*generalTestBoardParams)
		charToChangeTo = charSet["start"]  # initial board is filled with 'blocked'
		if exception is None:
			# fetch state of position on board
			b._get_tile(point)
		else:
			# equiv to "b._get_tile(point)"
			self.assertRaises(exception, b._get_tile, point)

	@parameterized.expand(parentsAndPaths)
	def test_get_path(self, parent, expectedPath):
		'''
1st test:
````````````
`***````````
`**&````````
`***````````
````````***`
````````&**`
````````***`
```****`````
```****`````
```****`````
````````````
````````````

2nd test:
````````````
`***````````
`**&````````
`***````````
````````***`
````*******`
````*```***`
```*&**`````
```****`````
```****`````
````````````
````````````
		'''
		b = Board(*generalTestBoardParams)
		actualPath = b._get_path(parent, (4, 7))
		self.assertEqual(expectedPath, actualPath)

	@parameterized.expand(parentsAndPaths)
	def test_get_path_returns_blank_list(self, parent, expectedPath):
		# same parent settings as above test, but now we request a point that isn't in parent
		b = Board(*generalTestBoardParams)
		actualPath = b._get_path(parent, (15, 15))
		self.assertEqual([], actualPath) # should return an empty list

	def test_init_board_resets_all_params(self):
		def extract_params(board):
			return copy.deepcopy(board._board), copy.deepcopy(board._rooms), \
					copy.deepcopy(board._autoconnect._edges), copy.deepcopy(board._autoconnect._invalidNeighbors)

		def perturb(board):
			# make changes to internal data structures
			board._change_tile((0, 0), "|")
			board.add_room(Room(4, 4, 4, 4))
			board._autoconnect.add_edge((0, 0), (2, 2))
			board._autoconnect.invalidate((0, 0), (2, 2))

		b = Board(*generalTestBoardParams)
		initialParams = extract_params(b)

		# change the params
		perturb(b)
		adjustedParams = extract_params(b)

		# make sure all params have changed
		for init, adj in zip(initialParams, adjustedParams):
			self.assertNotEqual(init, adj)

		# reset params to initial state
		b.init_board()
		afterInitParams = extract_params(b)

		# make sure the initial params are restored
		for init, adj in zip(initialParams, afterInitParams):
			self.assertEqual(init, adj)

	# TODO trying to A* from the very right side of the board, or the very bottom might cause a crash as it might end up exploring out of bounds
	# TODO I haven't acounted for negative values of x and y in the get tile or change tile
	@parameterized.expand(RoomPlacements)
	def test_room_is_outside_bounds(self, name, x, y, exception):
		b = Board(*generalTestBoardParams)
		room = Room(*generalRoomSize, x, y)

		if exception:
			self.assertRaises(exception, b.add_room, room)
		else:
			b.add_room(room)

	@parameterized.expand([r for r in RoomPlacements if r[-1] is None])
	def test_room_is_added(self, name, x, y, _):
		b = Board(*generalTestBoardParams)
		room = Room(*generalRoomSize, x, y)
		b.add_room(room)
		self.assertTrue(room in b._rooms)

	# shallow test because room.collide() is already tested very well
	def test_room_collision(self):
		b = Board(*generalTestBoardParams)
		room = Room(*generalRoomSize, 1, 1)
		b.add_room(room)

		# adding the room a second time raises exception
		self.assertRaises(RoomCollision, b.add_room, room)

	@parameterized.expand([
		["X and Y are just within bounds on the top left", 1, 1, boardState1],
		["Y is just within bounds on the bottom left", 1, generalTestBoardY - 6, boardState2],
		["X is just within bounds on the top right", generalTestBoardX - 6, 1, boardState3],
		["X and Y are just within bounds on the bottom right", generalTestBoardX - 6, generalTestBoardY - 6, boardState4],
	])
	def test_board_state_after_room_add(self, name, x, y, expectedBoardState):
		b = Board(*generalTestBoardParams)
		room = Room(*generalRoomSize, x, y)
		b.add_room(room)
		self.assertEqual(expectedBoardState, b._board)

	@parameterized.expand([
		["room 2 below room 1. Connect right anchor of room 1 to top anchor of room 2",
			Room(*generalRoomSize, 1, 1), Room(*generalRoomSize, 1, 10), (5, 3), (3, 10), boardState_connect_1],
		["room 2 to the right of room 1. Connect right anchor of room 1 to left anchor of room 2",
			Room(*generalRoomSize, 1, 1), Room(*generalRoomSize, 10, 1), (5, 3), (10, 3), boardState_connect_2],
		["room 2 to the right and below room 1. Connect right anchor of room 1 to right anchor of room 2",
			Room(*generalRoomSize, 1, 1), Room(*generalRoomSize, 10, 10), (5, 3), (14, 12), boardState_connect_3],
	])
	def test_board_state_after_connect_path_nodes(self, name, room1, room2, anchor1, anchor2, expectedBoard):
		b = Board(*generalTestBoardParams)
		b.add_room(room1)
		b.add_room(room2)

		self.assertTrue(b.connect_path_nodes(anchor1, anchor2))
		self.assertEqual(b._board, expectedBoard)


	@parameterized.expand([
		["room 2 below room 1. Connect right anchor of room 1 to top anchor of room 2",
			(3, 5), (12, 10), (5, 3), (14, 12), boardState_connect_complex_1],
		["room 2 to the right of room 1. Connect right anchor of room 1 to left anchor of room 2",
			(5, 3), (10, 12), (3, 5), (14, 12), boardState_connect_complex_2],
		["room 2 to the right and below room 1. Connect right anchor of room 1 to right anchor of room 2",
			(5, 3), (14, 12), (3, 5), (12, 10), boardState_connect_complex_3]
	])
	def test_board_state_after_connect_path_nodes_more_complex(self, name, anchor1, anchor2, anchor3, anchor4, expectedBoard):
		b = Board(*generalTestBoardParams)
		room1 = Room(*generalRoomSize, 1, 1)
		room2 = Room(*generalRoomSize, 10, 10)
		b.add_room(room1)
		b.add_room(room2)

		self.assertTrue(b.connect_path_nodes(anchor1, anchor2))
		self.assertTrue(b.connect_path_nodes(anchor3, anchor4))
		self.assertEqual(b._board, expectedBoard)


	@parameterized.expand([
		[(12, 15), (3, 5)],
		[(3, 5), (12, 15)],
	])
	def test_connect_path_nodes_failure_state(self, point1, point2):
		b = Board(*generalTestBoardParams)
		room1 = Room(*generalRoomSize, 1, 1)
		room2 = Room(*generalRoomSize, 10, 11)
		b.add_room(room1)
		b.add_room(room2)

		self.assertFalse(b.connect_path_nodes(point1, point2))

	def test_complex_case(self):

		expectedEdges = {(1, 2): {(3, 2): True, (2, 1): True, (2, 3): True}, (3, 2): {(1, 2): True, (2, 1): True, (2, 3): True, (4, 7): True}, (2, 1): {(1, 2): True, (3, 2): True, (2, 3): True}, (2, 3): {(1, 2): True, (3, 2): True, (2, 1): True}, (8, 5): {(10, 5): True, (9, 4): True, (9, 6): True, (4, 7): True}, (10, 5): {(8, 5): True, (9, 4): True, (9, 6): True}, (9, 4): {(8, 5): True, (10, 5): True, (9, 6): True}, (9, 6): {(8, 5): True, (10, 5): True, (9, 4): True}, (3, 8): {(6, 8): True, (4, 7): True, (4, 9): True}, (6, 8): {(3, 8): True, (4, 7): True, (4, 9): True}, (4, 7): {(3, 8): True, (6, 8): True, (4, 9): True, (8, 5): True, (3, 2): True}, (4, 9): {(3, 8): True, (6, 8): True, (4, 7): True}}
		expectedBoard = [['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '&', '*', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '&', '*', '-', '-', '-', '`', '`', '`', '`', '`', '`'], ['`', '*', '&', '*', '`', '-', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '-', '`', '`', '*', '&', '*', '`'], ['`', '`', '`', '`', '-', '-', '-', '-', '-', '*', '&', '`'], ['`', '`', '`', '`', '-', '`', '`', '`', '*', '&', '*', '`'], ['`', '`', '`', '*', '-', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '&', '*', '*', '&', '`', '`', '`', '`', '`'], ['`', '`', '`', '*', '&', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`']]
		expectedAnchors = [(1, 2), (3, 2), (2, 1), (2, 3), (8, 5), (10, 5), (9, 4), (9, 6), (3, 8), (6, 8), (4, 7), (4, 9)]

		b = Board(12, 12)
		b.add_room(Room(3, 3, 1, 1))
		b.add_room(Room(3, 3, 8, 4))
		b.add_room(Room(3, 4, 3, 7))

		b.connect_path_nodes((8, 5), (4, 7))
		b.connect_path_nodes((3, 2), (4, 7))

		self.assertEqual(expectedEdges, b._autoconnect._edges)
		self.assertEqual(expectedBoard, b._board)
		self.assertEqual(expectedAnchors, b._autoconnect._anchors)





if __name__ == '__main__':
	unittest.main()
