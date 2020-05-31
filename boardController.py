from board import Board
from room import Room
from settings import *
from random import randint, seed
from exceptions import *

class BoardController(object):
    def __init__(self, boardWidth=60, boardHeight=60, randomnessSeed=None):
        self.width = boardWidth
        self.height = boardHeight
        self.board = Board(boardWidth, boardHeight)

        self.randomnessSeed = randomnessSeed

        self.enemyController = None

    def fourRandomNumbers(self):
        height = randint(MIN_ROOM_HEIGHT, MAX_ROOM_HEIGHT)
        width = randint(MIN_ROOM_WIDTH, MAX_ROOM_WIDTH)
        positionX = randint(1, self.width - (width + 1))
        positionY = randint(1, self.height - (height + 1))
        return [height, width, positionX, positionY]

    #optional "randomnessSeed" integer for deterministic behavior
    def generateRandomMap(self):
        seed(self.randomnessSeed)
        for i in range(40):
            try:
                frn = self.fourRandomNumbers()
                self.board.add_room(Room(*frn))
            except RoomCollision:
                pass

        self.board.connect_board_automatically()

    def add_enemies(self):
        pass

    def play_player_moves(self):
        pass

    def play_enemy_moves(self):
        pass


    def draw_board(self):
        self.board.draw_board()