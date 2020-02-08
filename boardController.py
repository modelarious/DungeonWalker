from board import Board
from room import Room
from settings import *
from random import randint

class BoardController(object):
    def __init__(self, boardWidth=60, boardHeight=60):
        self.width = boardWidth
        self.height = boardHeight
        self.board = Board(boardWidth, boardHeight)

    def fourRandomNumbers(self):
        height = randint(MIN_ROOM_HEIGHT, MAX_ROOM_HEIGHT)
        width = randint(MIN_ROOM_WIDTH, MAX_ROOM_WIDTH)
        positionX = randint(1, self.width)
        positionY = randint(1, self.height)
        return [height, width, positionX, positionY]

    def generateRandomMap(self):

        MAX_ROOM_HEIGHT = 10
        MAX_ROOM_WIDTH = 10
        MIN_ROOM_WIDTH = 3
        MIN_ROOM_HEIGHT = 3
        for i in range(30):
            try:
                frn = self.fourRandomNumbers()
                self.board.add_room(Room(*frn))
            except:
                pass

        self.board.connect_board_automatically()

    def draw_board(self):
        self.board.draw_board()