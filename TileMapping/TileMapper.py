from models.MapModel import NeighborOffsets
from settings import charSet
from TileMapping.TileType import TileType
from TileMapping.TilePosition import TilePosition

class TileMapper:
    def __init__(self, mapModel, tileLoader):
        self._mapModel = mapModel
        self._tileLoader = tileLoader # XXX could be changed to a TileLoaderFactory later -> subclass RandomTileSetLoaderFactory that gives a random tileset
        self._tileArray = {} #pretends to be a 2d array that spans the entire map
    


    # some class that takes in the neighbors and then spits out the two keys Type and Position
	# then you just ask the TileLoader for the associated tile

	# XXX NO!!! ASk the TileLoader to figure it out for you, it will ask each tile if that arrangement
	# of blocks corresponds to them (so when the given tile is completely surrounded by blocked
	# tiles, then the Center Wall tile will call dibs).

	# XXX Tile mapper asks Map Model to get neighbors, then asks tileLoader what tile to use there and stores it
    # XXX * 2 - this is a good candidate for multi threading
    def process_board(self):
        print("processing tileset")
        for point in self._mapModel:
            
            x, y = point
            if x not in self._tileArray:
                self._tileArray[x] = {}
            neighbs = self._mapModel.get_all_eight_surrounding_neighbors_and_self(point)

            # center wall piece if all surrounding pieces are blocked XXX should be handled by a centerWall class
            if all(neighbs[t] == charSet["blocked"] for t in neighbs.keys()):
                self._tileArray[x][y] = self._tileLoader.get_tile(TileType.WALL, TilePosition.CENTER)
            # else:
            #     self._tileArray[x][y] = self._tileLoader.get_tile(TileType., TilePosition.CENTER)
            # if neighbs[NeighborOffsets.CENTER_MIDDLE] != charSet["blocked"]:
                # print(neighbs)
        print("done processing tileset")
    
    def get_tile_mapping(self):
        # XXX just for now, we don't have mappings for all the tiles
        out = []
        for x in self._tileArray:
            for y in self._tileArray[x]:
                out.append( ((x, y), self._tileArray[x][y]) )
        return out





# def crop(infile,height,width):
#     im = Image.open(infile)
#     imgwidth, imgheight = im.size
#     for i in range(imgheight//height):
#         for j in range(imgwidth//width):
#             box = (j*width, i*height, (j+1)*width, (i+1)*height)
#             yield im.crop(box)

# def get_stairs_one(image):
#     top = 387
#     left = 13
#     grid_size = 24
#     return crop_and_resize_square_image(image, top, left, grid_size)

# def get_stairs_two(image):
#     top = 387
#     left = 13
#     grid_size = 24
#     return crop_and_resize_square_image(image, top, left, grid_size)



from TileMapping.TileType import TileType
from TileMapping.TilePosition import TilePosition
from PIL import Image
import pygame
from TileMapping.TileLoader import TileLoader


if __name__ == "__main__":

    infile2 = "assets/tilesets/world abyss.png"
    with Image.open(infile2) as i:
        tileTypeToColumnNumberAssignments = {
            TileType.WALL: 1,
            TileType.GROUND: 4
        }
        tileLoader = TileLoader(i, tileTypeToColumnNumberAssignments)

        game_screen = pygame.display.set_mode((1024, 768))
        while True:
            for event in pygame.event.get():
                tt = TileType.GROUND
                x = 0
                y = 0

                for tp in TilePosition:
                    t = tileLoader.get_tile(tt, tp)
                    game_screen.blit(t, (x, y))
                    if x == 64:
                        x = 0
                        y += 32
                    else:
                        x += 32

                pygame.display.flip()


# get tile should take a Type and a Position:
# Type: GROUND, WALL, etc
# Position: UPPER_LEFT_CORNER, CENTER, etc...
# then these can be constants and you can dynamically populate the tile manager using them
# to makes sure that the contents of the tile manager line up with the constants you'll use to access it

# going to need two objects at least:
# - object that handles loading all the tiles from a tileset file
# - object that handles reading in the map, mapping the correct tiles to the 
#   right positions and holding that result in a 2d array, of which a 2x2 
#   box of tiles can be selected to be returned (step towards the camera feature)