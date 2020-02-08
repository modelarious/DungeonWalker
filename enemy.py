from queue import Queue


class Enemy(object):
    def __init__(self, board):
        self._inputQueue = Queue()
        self.board = board

    def decide_on_move(self):
        return "w"


