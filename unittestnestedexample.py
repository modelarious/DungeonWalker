import unittest
from settings import *
boards = [         
	["small width", (minBoardSize, modestBoardSize)],
        ["small height", (modestBoardSize, minBoardSize)],
        ["both small", (minBoardSize, minBoardSize)],
        ["modest sized", (modestBoardSize, modestBoardSize)]
]

#rooms = 
def test_generator(a):
    def test():
        assert a % 2 == 0
    return test

suite = unittest.TestSuite()
test_cases = [1, 2, 3, 4]
for case in test_cases:
    suite.addTest(
        unittest.FunctionTestCase(
            test_generator(case)))

unittest.TextTestRunner().run(suite)
