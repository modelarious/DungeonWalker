# thrown when given room dimensions are too large
class RoomTooLarge(Exception):
        pass

# thrown when given room dimensions are too small
class RoomTooSmall(Exception):
        pass

# thrown when a room given to the board would be outside the boundaries
class RoomOutsideBoard(Exception):
        pass

# thrown when a room given to the board collides with another room
class RoomCollision(Exception):
        pass

# thrown when the board is given paramaters that are too small
class BoardTooSmall(Exception):
        pass

#thrown when a point is outside the board
class PointOutsideBoard(Exception):
	pass
