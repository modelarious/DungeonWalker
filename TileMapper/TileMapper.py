from PIL import Image
import pygame

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
class TileLoader:
    def __init__(self, tilesetImage, tileTypeToColumnNumberAssignments):
        # data structure
        self.tiles = []
        self.tileIndex = {} # string -> index_to_tiles_array
        
        # useful local constants
        self.image = tilesetImage
        self.grid_size = 24 # each of the square tiles are 24 pixels wide
        self.border = 1 # there is a 1 pixel border around each of the individual square tiles. This border is shared (so the right border of one tile is the left border of the adjacent tile)
        self.scale_factor = self.grid_size + self.border # so to jump to the next tile, you need to move the tile width (grid_size) + the size of the shared border (border)

        # perform load of the tileset into the data structures
        self._populate_data(tileTypeToColumnNumberAssignments)

    def get_tile(self, tileType, tilePosition):
        arrayIndex = self.tileIndex[tileType][tilePosition]
        return self.tiles[arrayIndex]

    # perform load of the tileset into the data structures
    def _populate_data(self, tileTypeToColumnNumberAssignments):        
        # populate the requested tile types from the requested columns
        for tileType, columnNumber in tileTypeToColumnNumberAssignments.items():
            self.tileIndex[tileType] = {}
            self._populate_from_column(tileType, columnNumber)
    
    def _add_tile(self, tileType, tilePosition, tile):
        self.tileIndex[tileType][tilePosition] = len(self.tiles)
        self.tiles.append(self._export_for_pygame(tile))

    # translate from PIL to pygame so the tile can be drawn to the screen
    def _export_for_pygame(self, tile):
        strFormat = 'RGBA'
        # https://riptutorial.com/pygame/example/21220/using-with-pil fetched on July 13, 2020
        rawBytesTile = tile.tobytes("raw", strFormat)
        pygameTile = pygame.image.fromstring(rawBytesTile, tile.size, strFormat)
        return pygameTile

    # fetches the legend from the file
    def _populate_from_column(self, tileType, columnNumber):

        # XXX these could likely be member variables
        top = 162
        left = 8

        # move to the requested column
        left += self.scale_factor * 3 * columnNumber

        # get first 3x3 of values (standard pieces)
        tiles = self._get_three_by_three_tile_matrix(left, top)
        for t, pos in zip(tiles, TilePosition):
            self._add_tile(tileType, pos, t)

        # skip down to the next 3x3 of tiles
        top += self.scale_factor * 3
        # XXX fetch more advanced pieces (going to need a reflection algo for some tiles, and ability to ignore empty tiles that haven't been reflected)
    
    def _get_three_by_three_tile_matrix(self, leftX, topY):

        # ignore the border on the left and top
        startX = leftX + self.border
        startY = topY + self.border

        tiles = []

        # range to 3*scale_factor because we are grabbing 3 squares
        for y_dim in range(startY, startY + 3*self.scale_factor, self.scale_factor):
            for x_dim in range(startX, startX + 3*self.scale_factor, self.scale_factor):
                tile = self._crop_and_resize_square_image(y_dim, x_dim)
                tiles.append(tile)
        
        return tiles

    def _crop_and_resize_square_image(self, top, left):
        right = left + self.grid_size
        bottom = top + self.grid_size
        box = (left, top, right, bottom)
        cropped = self.image.crop(box)
        desiredSize = (32, 32)
        resized = cropped.resize(desiredSize)
        return resized

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