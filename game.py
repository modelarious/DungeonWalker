from boardController import BoardController


class Game(object):

    def __init__(self, boardWidth=60, boardHeight=60):
        self.boardController = BoardController(boardWidth, boardHeight)
        self.boardController.generateRandomMap()

    def draw_board(self):
        self.boardController.draw_board()


