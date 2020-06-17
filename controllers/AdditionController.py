from settings import charSet
from exceptions import RoomOutsideBoard

# model sits inside an "AdditionController" for lack of better name
# the MapGenerator tells the AdditionController what it wants done to the board
# the AdditionController then goes and calls things like change_tile()
class AdditionController():
    def __init__(self, mapModel):
        self.board = mapModel
        self.width = mapModel.getWidth()
        self.height = mapModel.getHeight()

    def setGoalSpace(self, pt):
        self.board.change_tile(pt, charSet["goal"])

    def setStartSpace(self, pt):
        self.board.change_tile(pt, charSet["start"])

    #XXX could use point_in_board?
    def _room_is_outside_bounds(self, room):
        if room.rightX > self.width - 1:
            return f"room.rightX ({room.rightX}) > self.width - 1 ({self.width - 1})"
        if room.leftX < 1:
            return f"room.leftX ({room.leftX}) < 1"
        if room.bottomY > self.height - 1:
            return f"room.bottomY ({room.bottomY}) > self.height - 1 ({self.height - 1})"
        if room.topY < 1:
            return f"room.topY ({room.topY}) < 1"
        return ""
    
    # raises exceptions for cases where:
    # - the room would leave the bounds of the board
    # - the room would collide with another that already exists
    def add_room(self, room):

        # raise an exception if the rectangle would leave the bounds of the board
        # XXX move most exception checking into the mapModel
        outOfBounds = self._room_is_outside_bounds(room)
        if outOfBounds:
            raise RoomOutsideBoard(outOfBounds)

        # add the room to the board
        # XXX let the board handle adding a room to itself - done here
        # XXX anytime change_tile is called, it should be from within the mapModel itself - done here
        for x in range(room.leftX, room.rightX):
            for y in range(room.topY, room.bottomY):
                point = (x, y)
                self.board.change_tile(point, charSet["passable"])

        # add the anchors to the board
        for anchor in room.getAnchors():
            self.board.change_tile(anchor, charSet["anchor"])
    
    def add_path(self, path):
        for node in path:
            self.board.change_tile(node, charSet["pathTemp"])

    # XXX tons of api overhead cause it will call this a ton of 
    # times while doing a* and the like
    def get_point(self, pt):
        return self.board.get_tile(pt)
    
    def get_neighbors(self, currPoint):
        if self.point_in_board(currPoint):
            currX, currY = currPoint
            offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))
            candidates = [(currX + offX, currY + offY) for offX, offY in offsets]
            candidates = list(filter(self.board.point_in_board, candidates))
            return candidates

        return []
    
    def point_in_board(self, pt):
        return self.board.point_in_board(pt)