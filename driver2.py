from room import Room
from board import Board
from random import randint

def fourRandomNumbers():
    return [randint(4, 10), randint(4, 10), randint(1, 60), randint(1, 60)]

if __name__ == '__main__':
    b = Board(60, 60)

    for i in range(30):
        try:
            frn = fourRandomNumbers()
            b.add_room(Room(*frn))
            print(f"b.add_room(Room(*{frn}))")
        except:
            pass


    print(b.connect_board_automatically())
    b.draw_board()
