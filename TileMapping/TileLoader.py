from TileMapping.TileType import TileType
from TileMapping.TilePosition import TilePosition
import pygame
from PIL import Image

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