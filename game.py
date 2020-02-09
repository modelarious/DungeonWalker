from boardController import BoardController


class Game(object):

    def __init__(self, boardWidth=60, boardHeight=60, randomnessSeed=None):
        self.boardController = BoardController(boardWidth, boardHeight, randomnessSeed)
        self.boardController.generateRandomMap()
        self.boardController.draw_board()

        self.boardController.add_enemies()
        self.game_loop()

    def draw_board(self):
        self.boardController.draw_board()

    def game_loop(self):
        while True:
            self.boardController.play_player_moves()
            self.boardController.play_enemy_moves()



