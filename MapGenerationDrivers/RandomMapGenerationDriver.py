from MapGenerationDrivers.MapGenerationDriverBaseClass import MapGenerationDriverBaseClass
from models.RoomModel import RoomModel
from settings import MIN_ROOM_HEIGHT, MAX_ROOM_HEIGHT, MIN_ROOM_WIDTH, MAX_ROOM_WIDTH
from random import randint, seed
from exceptions import RoomCollision

class RandomMapGenerationDriver(MapGenerationDriverBaseClass):
    def __init__(self, width, height, mapGeneratorEngine, randomnessSeed=11661):
        super().__init__(width, height, mapGeneratorEngine)
        if randomnessSeed == None:
            self.randomnessSeed = randint(0, 100000)
        else:
            self.randomnessSeed = randomnessSeed

    # generates 4 random numbers that are likely to result in parameters that
    # define a valid, placeable room
    # XXX make this based off boundary from additionController class
    def fourRandomNumbers(self):
        roomHeight = randint(MIN_ROOM_HEIGHT, MAX_ROOM_HEIGHT)
        roomWidth = randint(MIN_ROOM_WIDTH, MAX_ROOM_WIDTH)

        # generate X,Y for the top left corner of the room that will keep it 
        # within board boundaries
        positionX = randint(2, self.width - (roomWidth + 2))
        positionY = randint(2, self.height - (roomHeight + 2))
        return [roomHeight, roomWidth, positionX, positionY]

    #optional "randomnessSeed" integer for deterministic behavior
    def generateMap(self):
        print(self.randomnessSeed)
        seed(self.randomnessSeed)
        
        randomMapGenerationSuccess = False
        while not randomMapGenerationSuccess:
            for _ in range(600):
                try:
                    frn = self.fourRandomNumbers()
                    self.mapGeneratorEngine.add_room(RoomModel(*frn))
                except RoomCollision:
                    pass

            print("connecting board up")
            randomMapGenerationSuccess = self.mapGeneratorEngine.try_connect_board_automatically()
            print("connected up the board")
        return self.mapGeneratorEngine.get_finalized_board()