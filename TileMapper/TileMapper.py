from PIL import Image
import pygame
from time import sleep



# def crop(infile,height,width):
#     im = Image.open(infile)
#     imgwidth, imgheight = im.size
#     for i in range(imgheight//height):
#         for j in range(imgwidth//width):
#             box = (j*width, i*height, (j+1)*width, (i+1)*height)
#             yield im.crop(box)

def get_stairs_one(image):
    top = 387
    left = 13
    grid_size = 24
    return crop_and_resize_square_image(image, top, left, grid_size)

def get_three_by_three_tile_matrix(image, leftX, topY, grid_size, scale_factor, border):

    # ignore the border on the left and top
    startX = leftX + border
    startY = topY + border

    tiles = []

    # range to 3*scale_factor because we are grabbing 3 squares
    for x_dim in range(startX, startX + 3*scale_factor, scale_factor):
        for y_dim in range(startY, startY + 3*scale_factor, scale_factor):
            tile = crop_and_resize_square_image(image, y_dim, x_dim, grid_size)
            tiles.append(tile)
    
    return tiles

from enum import Enum
class TileType(Enum):
    GROUND = 1
    WALL = 2

class TilePosition(Enum):
    UPPER_LEFT_CORNER = 1
    UPPER_MIDDLE = 2
    UPPER_RIGHT_CORNER = 3
    MIDDLE_LEFT = 4
    CENTER = 5
    MIDDLE_RIGHT = 6
    BOTTOM_LEFT_CORNER = 7
    BOTTOM_MIDDLE = 8
    BOTTOM_RIGHT_CORNER = 9


# images are not hashable because they are mutable, so this is my solution that allows a hashmap
# to index an array of tiles instead
# XXX all the functionality in this file could likely fit in this class...
class TileManager:
    def __init__(self):
        self.tiles = []
        self.tileIndex = {} # string -> index_to_tiles_array

        # pre populate data container with blank objects
        for tileType in TileType:
            self.tileIndex[tileType] = {}
    
    def add_tile(self, tileType, tilePosition, tile):
        self.tileIndex[tileType][tilePosition] = len(self.tiles)
        self.tiles.append(self.export_for_pygame(tile))
    
    def get_tile(self, tileType, tilePosition):
        arrayIndex = self.tileIndex[tileType][tilePosition]
        return self.tiles[arrayIndex]
    
    def export_for_pygame(self, tile):
        strFormat = 'RGBA'
        # https://riptutorial.com/pygame/example/21220/using-with-pil fetched on July 13, 2020
        rawBytesTile = tile.tobytes("raw", strFormat)
        pygameTile = pygame.image.fromstring(rawBytesTile, tile.size, strFormat)
        return pygameTile


# fetches the legend from the file
def get_first_column(image):
    TM = TileManager()
    top = 162
    left = 8
    grid_size = 24 # each of the square tiles are 24 pixels wide
    border = 1 # there is a 1 pixel border around each of the individual square tiles. This border is shared (so the right border of one tile is the left border of the adjacent tile)

    scale_factor = grid_size + border # so to jump to the next tile, you need to move the tile width (grid_size) + the size of the shared border (border)

    # for testing, move over to the Walls column
    left += scale_factor * 3

    # get first 3x3 of values (the walls)
    tiles = get_three_by_three_tile_matrix(image, left, top, grid_size, scale_factor, border)
    for t, pos in zip(tiles, TilePosition):
        TM.add_tile(TileType.WALL, pos, t)
        # t.show()

    # skip down to the next 3x3 of tiles
    # top += scale_factor * 3

    # for testing, move over to the Ground column
    left += scale_factor * 3 * 3

    # get next 3x3 of values (the ground)
    ground = get_three_by_three_tile_matrix(image, left, top, grid_size, scale_factor, border)
    for t, pos in zip(ground, TilePosition):
        TM.add_tile(TileType.GROUND, pos, t)
        # t.show()
    
    return TM

# def get_stairs_two(image):
#     top = 387
#     left = 13
#     grid_size = 24
#     return crop_and_resize_square_image(image, top, left, grid_size)

def crop_and_resize_square_image(im, top, left, grid_size):
    right = left + grid_size
    bottom = top + grid_size
    box = (left, top, right, bottom)
    cropped = im.crop(box)
    desiredSize = (32, 32)
    resized = cropped.resize(desiredSize)
    return resized

infile2 = "assets/tilesets/world abyss.png"
with Image.open(infile2) as i:

    # XXX GROSS!!!!!!! Don't modify the tileManager inside a function.... make this whole thing into
    # a class, so you don't have to do dirty deeds
    tileManager = TileManager()
    TM = get_first_column(i)

    game_screen = pygame.display.set_mode((1024, 768))
    while True:
        for event in pygame.event.get():
            t = TM.get_tile(TileType.GROUND, TilePosition.CENTER)
            game_screen.blit(t, t.get_rect())
            game_screen.blit(t, (32, 0))
            game_screen.blit(t, (64, 0))
            game_screen.blit(t, (96, 0))

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