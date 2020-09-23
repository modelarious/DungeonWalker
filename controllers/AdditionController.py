from settings import charSet
from exceptions import RoomOutsideBoard

# model sits inside an "AdditionController" for lack of better name
# the MapGenerator tells the AdditionController what it wants done to the board
# the AdditionController then goes and calls things like change_tile()
# XXX AdditionEngine might be better.. but there's a better way to divide system responsibility
# XXX make this also responsible for adding paths
class AdditionController():

    def __init__(self, mapModel):
        self.board = mapModel
        self.width = mapModel.get_width()
        self.height = mapModel.get_height()
        self.boundarySize = 2

    def setGoalSpace(self, pt):
        self.board.set_goal_tile(pt)

    def setStartSpace(self, pt):
        self.board.set_starting_tile(pt)

    # defines a boundary of 2 squares around the entire board that is unusable when placing rooms.
    # this is so that paths have enough space to be drawn with a 1 space buffer from the nearest room
    def _fail_if_room_is_outside_bounds(self, room):
        outOfBoundsMessage = ""
        if room.rightX > self.width - self.boundarySize:
            outOfBoundsMessage = f"room.rightX ({room.rightX}) > self.width - {self.boundarySize} (boundary) ({self.width - self.boundarySize})"
        if room.leftX < self.boundarySize:
            outOfBoundsMessage = f"room.leftX ({room.leftX}) < {self.boundarySize} (boundary)"
        if room.bottomY > self.height - self.boundarySize:
            outOfBoundsMessage = f"room.bottomY ({room.bottomY}) > self.height - {self.boundarySize} (boundary) ({self.height - self.boundarySize})"
        if room.topY < self.boundarySize:
            outOfBoundsMessage = f"room.topY ({room.topY}) < {self.boundarySize} (boundary)"
        
        if outOfBoundsMessage:
            raise RoomOutsideBoard(outOfBoundsMessage)
    
    # raises exceptions for cases where:
    # - the room would leave the bounds of the board
    # - the room would collide with another that already exists
    def add_room(self, room):

        # raise an exception if the rectangle would leave the bounds of the board
        self._fail_if_room_is_outside_bounds(room)

        enemySpawnPoints = room.generate_spawn_points()

        # filter out player spawn point from list if it exists
        playerStartCoords = self.board.get_starting_coordinates()
        filteredEnemySpawnPoints = [e for e in enemySpawnPoints if e != playerStartCoords]

        self.board.add_enemy_spawn_points(filteredEnemySpawnPoints)

        # add the room to the board
        for x in range(room.leftX, room.rightX):
            for y in range(room.topY, room.bottomY):
                point = (x, y)
                self.board.change_tile(point, charSet["passable"])

        # add the anchors to the board
        for anchor in room.get_anchors():
            self.board.change_tile(anchor, charSet["anchor"])
    
    # draw every node in the path
    def add_path(self, path):
        for node in path:
            self.board.change_tile(node, charSet["pathTemp"])

    # XXX tons of api overhead cause it will call this a ton of 
    # times while doing a* and the like
    # XXX maybe the best solution would be to move the path finding stuff out 
    # of the engine and into this class
    def get_point(self, pt):
        return self.board.get_tile(pt)
    
    def get_neighbors_within_board(self, currPoint):
        return self.board.get_neighbors_within_board(currPoint)
    
    def point_in_board(self, pt):
        return self.board.point_in_board(pt)