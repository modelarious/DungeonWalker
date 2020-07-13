from PIL import Image
import pygame

def export_for_pygame(tilesetHash):
    strFormat = 'RGBA'
    exported = {}
    for description, tile in tilesetHash:

        # https://riptutorial.com/pygame/example/21220/using-with-pil fetched on July 13, 2020
        raw_str = tile.tostring("raw", strFormat)
        exported[description] = pygame.image.fromstring(raw_str, tile.size, strFormat)
    return exported

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
    return crop_square_image(image, top, left, grid_size)

def get_three_by_three_tile_matrix(image, leftX, topY, grid_size, scale_factor, border):

    # ignore the border on the left and top
    startX = leftX + border
    startY = topY + border

    tiles = []

    # range to 3*scale_factor because we are grabbing 3 squares
    for x_dim in range(startX, startX + 3*scale_factor, scale_factor):
        for y_dim in range(startY, startY + 3*scale_factor, scale_factor):
            tile = crop_square_image(image, y_dim, x_dim, grid_size)
            tiles.append(tile)
    
    return tiles

# images are not hashable because they are mutable, so this is my solution that allows a hashmap
# to index an array of tiles instead
# XXX all the functionality in this file could likely fit in this class...
class TileManager:
    def __init__(self):
        self.tiles = []
        self.tileIndex = {} # string -> index_to_tiles_array
    
    def add_tile(self, tile, title):
        self.tileIndex[title] = len(self.tiles)
        self.tiles.append(tile)
    
    def get_tile(self, title):
        arrayIndex = self.tileIndex[title]
        return self.tiles[arrayIndex]


# fetches the legend from the file
def get_first_column(image):
    top = 162
    left = 8
    grid_size = 24 # each of the square tiles are 24 pixels wide
    border = 1 # there is a 1 pixel border around each of the individual square tiles. This border is shared (so the right border of one tile is the left border of the adjacent tile)

    scale_factor = grid_size + border # so to jump to the next tile, you need to move the tile width (grid_size) + the size of the shared border (border)

    # for testing, move over to the Walls column
    left += scale_factor * 3

    # get first 3x3 of values
    tiles = get_three_by_three_tile_matrix(image, left, top, grid_size, scale_factor, border)
    for t in tiles:
        t.show()

    # skip down to the next 3x3 of tiles
    top += scale_factor * 3

    ground = get_three_by_three_tile_matrix(image, left, top, grid_size, scale_factor, border)
    for t in ground:
        t.show()
    
    return {tileCount: element for element, tileCount in enumerate(ground)}

# def get_stairs_two(image):
#     top = 387
#     left = 13
#     grid_size = 24
#     return crop_square_image(image, top, left, grid_size)

def crop_square_image(im, top, left, grid_size):
    right = left + grid_size
    bottom = top + grid_size
    box = (left, top, right, bottom)
    return im.crop(box)



# infile = "assets/tilesets/stairs.png"
# with Image.open(infile) as i:
#     stairs1 = get_stairs_one(i)
#     stairs1.show()

infile2 = "assets/tilesets/world abyss.png"
with Image.open(infile2) as i:
    get_first_column(i)
    