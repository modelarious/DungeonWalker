from game import Game

g = Game(randomnessSeed=5)
g.draw_board()

g.boardController.board.play_move((18,2), (1,1))

g.draw_board()
