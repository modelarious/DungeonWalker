from room import Room
from board import Board
if __name__ == '__main__':
    b = Board(12, 12)

    '''
`````````````
`*&*`````````
`&*&`````````
`*&*`````*&*`
`````````&*&`
`````````*&*`
`````````````
```*&**``````
```&**&``````
```*&**``````
`````````````
    '''

    b.add_room(Room(3, 3, 1, 1))
    b.add_room(Room(3, 3, 8, 4))
    b.add_room(Room(3, 4, 3, 7))
    '''
roomHeight, roomWidth = (4, 5)
topLeftX, topLeftY = (3,1)

r = Room(roomHeight, roomWidth, topLeftX, topLeftY)
x.add_room(r)

x.add_room(r)
    '''

    b.draw_board()

    p1 = (8, 5)
    # p1 = (3, 2)
    p2 = (4, 7)
    b.connect_path_nodes(p1, p2)
    b.draw_board()
    p1 = (3, 2)
    # p1 = (8, 5)
    b.connect_path_nodes(p1, p2)

    b._finalize_board()
    b.draw_board()
    print("edges:", b._autoconnect._edges)
    print("board:", b._board)
    print("anchors:", b._autoconnect._anchors)
