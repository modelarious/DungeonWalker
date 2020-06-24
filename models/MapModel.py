from settings import MIN_BOARD_WIDTH, MIN_BOARD_HEIGHT, charSet
from exceptions import PointOutsideBoard, BoardTooSmall
from copy import copy
from models.PlayerCharacterModel import PlayerCharacterModel

class MapModel():
    def __init__(self, width, height):
        if width < MIN_BOARD_WIDTH or height < MIN_BOARD_HEIGHT: raise BoardTooSmall

        self.width = width
        self.height = height

        self._board = self._create_empty_board()
    
    def _create_empty_board(self):
        board = []
        for y in range(self.height):
            blankRow = [charSet["blocked"]]*self.width
            board.append(blankRow)
        return board
    
    def get_board(self):
        return self._board
    
    def get_tile(self, point):
        pX, pY = point
        if not self.point_in_board(point):
            raise PointOutsideBoard(
                f"get_tile: board width and height ({self.width}, {self.height}), given point: ({pX, pY})")
        return self._board[pY][pX]

    def change_tile(self, point, char):
        pX, pY = point
        if not self.point_in_board(point):
            raise PointOutsideBoard(
                f"change_tile: board width and height ({self.width}, {self.height}), given point: ({pX, pY})")
        self._board[pY][pX] = char

    def point_in_board(self, pt):
        (pX, pY) = pt
        if pX < 0 or pY < 0:
            return False
        try:
            self._board[pY][pX]
            return True
        except IndexError:
            return False
    
    # print the board to the screen (used to quickly verify the view)
    def draw_board(self):
        for row in self._board:
            row = list(map(lambda a : a.get_char(), row))
            print("".join(row).replace(charSet["pathTemp"].get_char(), charSet["passable"].get_char())
                .replace(charSet["anchor"].get_char(), charSet["passable"].get_char()))
        print()
    
    def get_width(self):
        return copy(self.width)
    
    def get_height(self):
        return copy(self.height)
    
    def get_start_tile(self):
        return PENIS
