import unittest

from models.MapModel import MapModel as Board
from models.RoomModel import RoomModel as Room
from helpers.Autoconnect import Autoconnect
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

# negative indices
pointTests.append(["X is negative", (-1, 1), PointOutsideBoard])
pointTests.append(["Y is negative", (1, -1), PointOutsideBoard])


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

def boardFactory(boardParams):
	return Board(*boardParams, Autoconnect())


class TestBoardCreation(unittest.TestCase):
	@parameterized.expand([
		["small width", (minBoardSize, modestBoardSize)],
		["small height", (modestBoardSize, minBoardSize)],
		["both small", (minBoardSize, minBoardSize)],
		["modest sized", (modestBoardSize, modestBoardSize)]
	])
	def test_correct_board_creation(self, name, boardParams):
		b = boardFactory(boardParams)
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
		b = boardFactory(generalTestBoardParams)
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
		b = boardFactory(generalTestBoardParams)
		charToChangeTo = charSet["start"]  # initial board is filled with 'blocked'

		if exception is None:
			# change state of position on board
			b._change_tile(point, charToChangeTo)
		else:
			# equiv to "b._change_tile(point, charToChangeTo)"
			self.assertRaises(exception, b._change_tile, point, charToChangeTo)

	@parameterized.expand(pointTests)
	def test_board_get_tile_range(self, name, point, exception):
		b = boardFactory(generalTestBoardParams)
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
		b = boardFactory(generalTestBoardParams)
		actualPath = b._get_path(parent, (4, 7))
		self.assertEqual(expectedPath, actualPath)

	@parameterized.expand(parentsAndPaths)
	def test_get_path_returns_blank_list(self, parent, expectedPath):
		# same parent settings as above test, but now we request a point that isn't in parent
		b = boardFactory(generalTestBoardParams)
		actualPath = b._get_path(parent, (15, 15))
		self.assertEqual([], actualPath) # should return an empty list

	# def test_init_board_resets_all_params(self):
	# 	def extract_params(board):
	# 		return copy.deepcopy(board._board), copy.deepcopy(board._rooms), \
	# 				copy.deepcopy(board._autoconnect._edges), copy.deepcopy(board._autoconnect._invalidNeighbors)

	# 	def perturb(board):
	# 		# make changes to internal data structures
	# 		board._change_tile((0, 0), "|")
	# 		board.add_room(Room(4, 4, 4, 4))
	# 		board._autoconnect.add_edge((0, 0), (2, 2))
	# 		board._autoconnect._invalidate((0, 0), (2, 2))

	# 	b = boardFactory(generalTestBoardParams)
	# 	initialParams = extract_params(b)

	# 	# change the params
	# 	perturb(b)
	# 	adjustedParams = extract_params(b)

	# 	# make sure all params have changed
	# 	for init, adj in zip(initialParams, adjustedParams):
	# 		self.assertNotEqual(init, adj)

	# 	# reset params to initial state
	# 	b.init_board()
	# 	afterInitParams = extract_params(b)

	# 	# make sure the initial params are restored
	# 	for init, adj in zip(initialParams, afterInitParams):
	# 		self.assertEqual(init, adj)

	# TODO trying to A* from the very right side of the board, or the very bottom might cause a crash as it might end up exploring out of bounds
	# TODO I haven't acounted for negative values of x and y in the get tile or change tile
	@parameterized.expand(RoomPlacements)
	def test_room_is_outside_bounds(self, name, x, y, exception):
		b = boardFactory(generalTestBoardParams)
		room = Room(*generalRoomSize, x, y)

		if exception:
			self.assertRaises(exception, b.add_room, room)
		else:
			b.add_room(room)

	@parameterized.expand([r for r in RoomPlacements if r[-1] is None])
	def test_room_is_added(self, name, x, y, _):
		b = boardFactory(generalTestBoardParams)
		room = Room(*generalRoomSize, x, y)
		b.add_room(room)
		self.assertTrue(room in b._rooms)

	# shallow test because room.collide() is already tested very well
	def test_room_collision(self):
		b = boardFactory(generalTestBoardParams)
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
		b = boardFactory(generalTestBoardParams)
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
		b = boardFactory(generalTestBoardParams)
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
		b = boardFactory(generalTestBoardParams)
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
		b = boardFactory(generalTestBoardParams)
		room1 = Room(*generalRoomSize, 1, 1)
		room2 = Room(*generalRoomSize, 10, 11)
		b.add_room(room1)
		b.add_room(room2)

		self.assertFalse(b.connect_path_nodes(point1, point2))

	def test_complex_case(self):

		expectedEdges = {(1, 2): {(3, 2): True, (2, 1): True, (2, 3): True}, (3, 2): {(1, 2): True, (2, 1): True, (2, 3): True, (4, 7): True}, (2, 1): {(1, 2): True, (3, 2): True, (2, 3): True}, (2, 3): {(1, 2): True, (3, 2): True, (2, 1): True}, (8, 5): {(10, 5): True, (9, 4): True, (9, 6): True, (4, 7): True}, (10, 5): {(8, 5): True, (9, 4): True, (9, 6): True}, (9, 4): {(8, 5): True, (10, 5): True, (9, 6): True}, (9, 6): {(8, 5): True, (10, 5): True, (9, 4): True}, (3, 8): {(6, 8): True, (4, 7): True, (4, 9): True}, (6, 8): {(3, 8): True, (4, 7): True, (4, 9): True}, (4, 7): {(3, 8): True, (6, 8): True, (4, 9): True, (8, 5): True, (3, 2): True}, (4, 9): {(3, 8): True, (6, 8): True, (4, 7): True}}
		expectedBoard = [['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '&', '*', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '&', '*', '-', '-', '-', '`', '`', '`', '`', '`', '`'], ['`', '*', '&', '*', '`', '-', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '-', '-', '`', '`', '*', '&', '*', '`'], ['`', '`', '`', '`', '-', '-', '-', '-', '-', '*', '&', '`'], ['`', '`', '`', '`', '-', '`', '`', '`', '*', '&', '*', '`'], ['`', '`', '`', '*', '-', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '&', '*', '*', '&', '`', '`', '`', '`', '`'], ['`', '`', '`', '*', '&', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`']]
		expectedAnchors = [(1, 2), (3, 2), (2, 1), (2, 3), (8, 5), (10, 5), (9, 4), (9, 6), (3, 8), (6, 8), (4, 7), (4, 9)]

		b = Board(12, 12, Autoconnect())
		b.add_room(Room(3, 3, 1, 1))
		b.add_room(Room(3, 3, 8, 4))
		b.add_room(Room(3, 4, 3, 7))

		b.connect_path_nodes((8, 5), (4, 7))
		b.connect_path_nodes((3, 2), (4, 7))

		self.assertEqual(expectedEdges, b._autoconnect._edges)
		self.assertEqual(expectedBoard, b._board)
		self.assertEqual(expectedAnchors, b._autoconnect._anchors)

	def test_get_neighbors_returns_empty_list(self):
		b = boardFactory(generalTestBoardParams)
		self.assertEqual([], b._get_neighbors((300, 300)))

	@parameterized.expand([
		[(300, 300), (1, 1)],
		[(1, 1), (300, 300)],
	])
	def test_depth_limited_search_returns_False(self, startPoint, endPoint):
		b = boardFactory(generalTestBoardParams)
		self.assertFalse(b._depth_limited_search(startPoint, endPoint))

	def test_draw_succeeds(self):
		b = boardFactory(generalTestBoardParams)
		b.draw_board()

	def test_connect_path_nodes_fails_when_going_negative(self):
		b = boardFactory(generalTestBoardParams)
		room1 = Room(*generalRoomSize, 1, 1)
		room2 = Room(*generalRoomSize, 14, 1)
		b.add_room(room1)
		b.add_room(room2)

		self.assertFalse(b.connect_path_nodes((1, 3), (18, 3)))

	# show that two rooms with anchors touching can be connected
	def test_connect_path_two_adjacent_rooms(self):
		r1 = Room(4, 5, 1, 1)  # 4 by 5 room at (1, 1)
		r2 = Room(4, 5, 6, 1)  # 4 by 5 room at (6, 1) (directly touching sides)
		board = Board(20, 20, Autoconnect())

		for r in [r1, r2]:
			board.add_room(r)

		self.assertTrue(board.connect_path_nodes((5, 2), (6, 2)))

	'''
````````````````````
`*****`*****````````
`*************``````
`*****`*****`*``````
`*r1**`*r2**`*``````
````````````**``````
````````````*```````
``````````*****`````
``````````*****`````
``````````*****`````
``````````*r3**`````
````````````````````
````````````````````
````````````````````
````````````````````
````````````````````
````````````````````
````````````````````
````````````````````
````````````````````
	'''
	def test_finalize_board(self):
		r1 = Room(4, 5, 1, 1)  # 4 by 5 room at (1, 1)
		r2 = Room(4, 5, 7, 1)  # 4 by 5 room at (7, 1) (separated from r1 by 1 space)
		r3 = Room(4, 5, 10, 7)  # 4 by 5 room at (10, 7)
		board = Board(20, 20, Autoconnect())

		for r in [r1, r2, r3]:
			board.add_room(r)

		#connect up r1 to r2 and r2 to r3
		self.assertTrue(board.connect_path_nodes((11, 2), (12, 7)))
		self.assertTrue(board.connect_path_nodes((5, 2), (7, 2)))

		board._finalize_board()
		expectedBoardState = [['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', 'S', '*', '*', '*', '-', '-', '-', '*', '*', '*', '-', '-', '-', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '`', '*', '*', '*', '*', '*', '`', '-', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '&', '*', '*', '`', '*', '*', '&', '*', '*', '`', '-', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '-', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '-', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '&', '*', '*', '*', 'G', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`']]
		self.assertEqual(board._board, expectedBoardState)

		'''
		r4 = Room(4, 5, 13, 14)
		board.add_room(r4)
		board.draw_board()

		print(r4.getAnchors())
		print(r1.getAnchors())

		board.connect_path_nodes((13, 15), (3, 4))
		board.draw_board()

		reachable, layers = board._autoconnect.get_reachable_nodes((1, 2))
		for depth, pts in layers.items():
			for pt in pts:
				board._change_tile(pt, str(depth))

		board.draw_board()
		'''

	def test_finalize_board_fails_with_no_rooms(self):
		b = Board(20, 20, Autoconnect())
		self.assertFalse(b._finalize_board())

	def test_run_hard_test(self):
		b = Board(60, 60, Autoconnect())
		b.add_room(Room(*[4, 9, 40, 47]))
		b.add_room(Room(*[7, 9, 11, 1]))
		b.add_room(Room(*[5, 7, 46, 30]))
		b.add_room(Room(*[5, 9, 16, 50]))
		b.add_room(Room(*[9, 5, 39, 13]))
		b.add_room(Room(*[9, 9, 27, 43]))
		b.add_room(Room(*[8, 4, 4, 36]))
		b.add_room(Room(*[8, 5, 52, 37]))
		b.add_room(Room(*[7, 4, 12, 20]))
		b.add_room(Room(*[6, 10, 25, 2]))
		b.add_room(Room(*[10, 4, 52, 17]))
		b.add_room(Room(*[9, 5, 51, 4]))
		b.add_room(Room(*[7, 5, 22, 23]))

		b.connect_path_nodes(*((4, 39), (4, 39)))
		b.connect_path_nodes(*((11, 4), (11, 4)))
		b.connect_path_nodes(*((12, 23), (12, 23)))
		b.connect_path_nodes(*((16, 52), (16, 52)))
		b.connect_path_nodes(*((22, 26), (22, 26)))
		b.connect_path_nodes(*((25, 4), (25, 4)))
		b.connect_path_nodes(*((27, 47), (27, 47)))
		b.connect_path_nodes(*((39, 17), (39, 17)))
		b.connect_path_nodes(*((40, 48), (40, 48)))
		b.connect_path_nodes(*((46, 32), (46, 32)))
		b.connect_path_nodes(*((51, 8), (51, 8)))
		b.connect_path_nodes(*((52, 21), (52, 21)))
		b.connect_path_nodes(*((52, 40), (52, 40)))
		b.connect_path_nodes(*((53, 12), (53, 17)))
		b.connect_path_nodes(*((19, 4), (25, 4)))
		b.connect_path_nodes(*((35, 47), (40, 48)))
		b.connect_path_nodes(*((52, 32), (53, 26)))
		b.connect_path_nodes(*((52, 32), (54, 37)))
		b.connect_path_nodes(*((24, 52), (31, 51)))
		b.connect_path_nodes(*((13, 26), (22, 26)))
		b.connect_path_nodes(*((43, 17), (53, 17)))
		b.connect_path_nodes(*((48, 48), (54, 44)))

		# previously caused a bug where it can't find a path
		b.connect_path_nodes(*((53, 26), (54, 37)))

	def test_second_hard_test(self):
		b = Board(60, 60)
		b.add_room(Room(*[9, 6, 11, 41]))
		b.add_room(Room(*[9, 5, 22, 8]))
		b.add_room(Room(*[6, 5, 23, 49]))
		b.add_room(Room(*[5, 10, 34, 51]))
		b.add_room(Room(*[4, 9, 23, 27]))
		b.add_room(Room(*[10, 7, 11, 8]))
		b.add_room(Room(*[4, 4, 5, 33]))
		b.add_room(Room(*[9, 10, 30, 11]))
		b.add_room(Room(*[8, 6, 50, 31]))
		b.add_room(Room(*[7, 4, 48, 46]))
		b.add_room(Room(*[7, 6, 36, 20]))
		b.add_room(Room(*[7, 7, 1, 15]))

		b.connect_path_nodes(*((17, 12), (22, 12)))
		b.connect_path_nodes(*((34, 19), (36, 23)))
		b.connect_path_nodes(*((24, 16), (30, 15)))
		b.connect_path_nodes(*((43, 53), (49, 52)))
		b.connect_path_nodes(*((7, 18), (14, 17)))
		b.connect_path_nodes(*((27, 51), (34, 53)))
		b.connect_path_nodes(*((31, 28), (38, 26)))
		b.connect_path_nodes(*((49, 46), (52, 38)))
		b.connect_path_nodes(*((6, 36), (13, 41)))
		b.connect_path_nodes(*((13, 49), (23, 51)))
		b.connect_path_nodes(*((4, 21), (5, 34)))


	def test_second_hard_test(self):
		b = Board(60, 60, Autoconnect())
		b.add_room(Room(*[9, 6, 11, 41]))
		b.add_room(Room(*[9, 5, 22, 8]))
		b.add_room(Room(*[6, 5, 23, 49]))
		b.add_room(Room(*[5, 10, 34, 51]))
		b.add_room(Room(*[4, 9, 23, 27]))
		b.add_room(Room(*[10, 7, 11, 8]))
		b.add_room(Room(*[4, 4, 5, 33]))
		b.add_room(Room(*[9, 10, 30, 11]))
		b.add_room(Room(*[8, 6, 50, 31]))
		b.add_room(Room(*[7, 4, 48, 46]))
		b.add_room(Room(*[7, 6, 36, 20]))
		b.add_room(Room(*[7, 7, 1, 15]))

		b.connect_board_automatically()
		expectedBoard = [['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '&', '*', '*', '*', '`', '`', '`', '`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '`', '`', '*', '*', '*', '*', '&', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '&', '*', '*', '*', '*', '*', '-', '-', '-', '-', '-', '-', '*', '*', '*', '&', '`', '`', '`', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '`', '`', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '`', '`', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '&', '*', '*', '*', '`', '`', '`', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '-', '-', '-', '*', '*', '*', '*', '*', '*', '*', '*', '&', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '*', '*', '-', '*', '*', '`', '-', '`', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '*', '*', '*', '-', '*', '*', '*', '`', '`', '`', '`', '`', '`', '-', '`', '`', '-', '-', '`', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '&', '*', '*', '*', '*', '*', '-', '-', '-', '-', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '-', '-', '-', '`', '`', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '*', '*', '`', '`', '-', '-', '-', '-', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '-', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '`', '*', '*', '&', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '*', '*', '*', '-', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '`', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '`', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '-', '-', '*', '*', '*', '*', '&', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '-', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', 'G', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '&', '*', '*', '*', '*', '*', '*', '*', '-', '-', '-', '-', '-', '-', '-', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '&', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '&', '*', '*', '*', '`', '`', '`', '`'], ['`', '`', '`', '-', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`'], ['`', '`', '`', '-', '`', '*', '&', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`'], ['`', '`', '`', '-', '-', '-', '*', '*', '&', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '&', '*', '*', '*', '*', '&', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '*', '-', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '-', '*', '*', '*', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '-', '-', '-', '-', '-', '-', '-', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '-', '-', '-', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '-', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '&', '*', '*', '*', '*', '&', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '-', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', 'S', '*', '*', '*', '`', '`', '`', '`', '`', '`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '&', '*', '*', '&', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '*', '*', '*', '-', '-', '-', '`', '`', '`', '`', '*', '*', '*', '*', '&', '*', '*', '*', '*', '*', '`', '`', '`', '`', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '-', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '`', '*', '-', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '`', '-', '-', '-', '-', '-', '-', '*', '*', '*', '*', '*', '*', '*', '*', '-', '-', '-', '-', '-', '`', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '&', '*', '*', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '`', '`', '`', '-', '-', '-', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '*', '*', '*', '*', '&', '*', '*', '*', '*', '*', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`'], ['`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`', '`']]
		self.assertEqual(expectedBoard, b._board)



if __name__ == '__main__':
	unittest.main()