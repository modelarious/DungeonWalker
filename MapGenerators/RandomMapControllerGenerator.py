from MapGenerators.MapGeneratorControllerBaseClass import MapGeneratorControllerBaseClass
from models.RoomModel import RoomModel
from settings import MIN_ROOM_HEIGHT, MAX_ROOM_HEIGHT, MIN_ROOM_WIDTH, MAX_ROOM_WIDTH
from random import randint, seed
from exceptions import RoomCollision

class RandomMapControllerGenerator(MapGeneratorControllerBaseClass):
    def __init__(self, width, height, mapGenerator, randomnessSeed=4):
        super().__init__(width, height, mapGenerator)
        self.randomnessSeed = randomnessSeed

    # generates 4 random numbers that are likely to result in parameters that
    # define a valid, placeable room
    def fourRandomNumbers(self):
        roomHeight = randint(MIN_ROOM_HEIGHT, MAX_ROOM_HEIGHT)
        roomWidth = randint(MIN_ROOM_WIDTH, MAX_ROOM_WIDTH)
        positionX = randint(1, self.width - (roomWidth + 1))
        positionY = randint(1, self.height - (roomHeight + 1))
        return [roomHeight, roomWidth, positionX, positionY]

    #optional "randomnessSeed" integer for deterministic behavior
    def generateMap(self):
        seed(self.randomnessSeed)
        for _ in range(6):
            try:
                frn = self.fourRandomNumbers()
                self.mapGenerator.add_room(RoomModel(*frn))
            except RoomCollision:
                pass

        self.mapGenerator.connect_board_automatically()
        return self.mapGenerator.XXX_SPIT_OUT_BOARD()