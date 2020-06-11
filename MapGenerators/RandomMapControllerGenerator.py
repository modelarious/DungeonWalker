from MapGenerators.MapGeneratorControllerBaseClass import MapGeneratorControllerBaseClass
from models.RoomModel import RoomModel
from settings import MIN_ROOM_HEIGHT, MAX_ROOM_HEIGHT, MIN_ROOM_WIDTH, MAX_ROOM_WIDTH
from random import randint, seed
from exceptions import RoomCollision

class RandomMapControllerGenerator(MapGeneratorControllerBaseClass):
    def fourRandomNumbers(self):
        height = randint(MIN_ROOM_HEIGHT, MAX_ROOM_HEIGHT)
        width = randint(MIN_ROOM_WIDTH, MAX_ROOM_WIDTH)
        positionX = randint(1, self.mapGenerator.width - (width + 1))
        positionY = randint(1, self.mapGenerator.height - (height + 1))
        return [height, width, positionX, positionY]

    #optional "randomnessSeed" integer for deterministic behavior
    def generateMap(self):
        seed(1)
        for _ in range(6):
            try:
                frn = self.fourRandomNumbers()
                self.mapGenerator.add_room(RoomModel(*frn))
            except RoomCollision:
                pass

        self.mapGenerator.connect_board_automatically()
        return self.mapGenerator.XXX_SPIT_OUT_BOARD()