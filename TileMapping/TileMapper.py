class TileMapper:
    def __init__(self, mapModel, tileLoader):
        self.board = mapModel
        self.tileLoader = tileLoader # XXX could be changed to a TileLoaderFactory later -> subclass RandomTileSetLoaderFactory that gives a random tileset

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