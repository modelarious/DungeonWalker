import unittest

from board import Board
from room import Room
from autoconnect import Autoconnect
from exceptions import *
from settings import *
from parameterized import parameterized

pointsAndExpectedNeighbors = [
        [(1, 2), {(5, 2): True, (3, 1): True, (3, 4): True}],
        [(5, 2), {(1, 2): True, (3, 1): True, (3, 4): True}],
        [(3, 1), {(1, 2): True, (5, 2): True, (3, 4): True}],
        [(3, 4), {(1, 2): True, (5, 2): True, (3, 1): True}]
]

class TestAutoConnect(unittest.TestCase):
    #add a room. All the anchors should be connected to each other within the room
    @parameterized.expand(pointsAndExpectedNeighbors)
    def test_get_neighbors_single_room(self, point, expectedNeighbors):
        a = Autoconnect()
        r = Room(4,5, 1,1) # 4 by 5 room at (1, 1)
        a.add_anchors(r)
        self.assertEqual(a.get_neighbors(point), expectedNeighbors)

    #put room1 and room2 such that their anchors touch each other, but aren't
    #connected.  We are saying that these aren't neighbors as they haven't
    #been formally connected
    @parameterized.expand(pointsAndExpectedNeighbors)
    def test_get_neighbors_touching_rooms(self, point, expectedNeighbors):
        a = Autoconnect()
        r1 = Room(4, 5, 1, 1) # 4 by 5 room at (1, 1)
        r2 = Room(4, 5, 6, 1)  # 4 by 5 room at (6, 1) (directly touching sides)
        a.add_anchors(r1)
        a.add_anchors(r2)
        '''
        board = Board(20, 20)
        for r in [r1, r2]:
            board.add_room(r)
        board.draw_board()
        '''
        self.assertEqual(a.get_neighbors(point), expectedNeighbors)

    #don't connect room 1 to room2 or 3, but connect up room 2 and 3
    #then check that room 1 points still have the same neighbors
    @parameterized.expand(pointsAndExpectedNeighbors)
    def test_get_neighbors_three_room_two_connect(self, point, expectedNeighbors):
        a = Autoconnect()
        r1 = Room(4, 5, 1, 1) # 4 by 5 room at (1, 1)
        r2 = Room(4, 5, 6, 1)  # 4 by 5 room at (6, 1) (directly touching sides)
        r3 = Room(4, 5, 10, 7)  # 4 by 5 room at (10, 7)
        a.add_anchors(r1)
        a.add_anchors(r2)
        a.add_anchors(r3)

        '''
        board = Board(20, 20)
        for r in [r1, r2, r3]:
            board.add_room(r)
        self.assertTrue(board.connect_path_nodes((10,2), (12, 7)))
        board.draw_board()
        '''

        a.add_edge((10, 2), (12, 7))
        self.assertEqual(a.get_neighbors(point), expectedNeighbors)

        #print(a.get_reachable_nodes((10,2)))
        #self.assertEqual(a.get_reachable_nodes((10,2)),
        #                [(6, 2), (8, 1), (8, 4), (12, 7), (10, 8), (14, 8), (12, 10)])

    #connect up rooms 1 2 and 3, check that they're all reachable from any node
    def test_get_neighbors_three_room_all_connect(self):
        a = Autoconnect()
        r1 = Room(4, 5, 1, 1) # 4 by 5 room at (1, 1)
        r2 = Room(4, 5, 7, 1)  # 4 by 5 room at (6, 1) (directly touching sides)
        r3 = Room(4, 5, 10, 7)  # 4 by 5 room at (10, 7)
        a.add_anchors(r1)
        a.add_anchors(r2)
        a.add_anchors(r3)

        a.add_edge((11, 2), (12, 7))
        a.add_edge((5, 2), (7, 2))
        reachable, layers = a.get_reachable_nodes((11, 2))
        #self.assertEqual(reachable, [(10, 2), (6, 2), (8, 1), (8, 4), (12, 7), (5, 2), (10, 8), (14, 8), (12, 10), (1, 2), (3, 1), (3, 4)])
        print(reachable, layers)

        board = Board(20, 20)
        for r in [r1, r2, r3]:
            board.add_room(r)
        self.assertTrue(board.connect_path_nodes((11, 2), (12, 7)))
        self.assertTrue(board.connect_path_nodes((5, 2), (7, 2)))
        board.draw_board()
        board._finalize_board()

        for depth, pts in layers.items():
            for pt in pts:
                board._change_tile(pt, str(depth))

        board.draw_board()
        expectedReachable = [(11, 2), (7, 2), (9, 1), (9, 4), (12, 7), (7, 2), (5, 2), (9, 1), (9, 4), (12, 7), (10, 8), (14, 8), (12, 10), (5, 2), (1, 2), (3, 1), (3, 4), (10, 8), (14, 8), (12, 10), (1, 2), (3, 1), (3, 4)]
        expectedLayers = {0: [(11, 2)], 1: [(7, 2), (9, 1), (9, 4), (12, 7)], 2: [(5, 2), (10, 8), (14, 8), (12, 10)], 3: [(1, 2), (3, 1), (3, 4)]}

        self.assertEqual(expectedReachable, reachable)
        self.assertEqual(expectedLayers, layers)

# a.add_edge((10,2), ())
if __name__ == '__main__':
	unittest.main()