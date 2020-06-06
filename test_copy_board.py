import unittest

from helpers.Autoconnect import Autoconnect
from models.MapModel import MapModel as Board
import copy

class TestCopyBoard(unittest.TestCase):
    def test_correct_board_creation(self):
        oldVal = 40
        newVal = 300
        b = Board(oldVal, 35, Autoconnect())
        b2 = b.get_copy()

        b2.width = newVal
        assert b.width == oldVal


