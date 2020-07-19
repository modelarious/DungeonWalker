from TileMapping.TileType import TileType
from TileMapping.TilePosition import TilePosition
import pygame
from PIL import Image

# XXX remove
class TileContainer:
	''' 
	keep associated pieces of data together, and make it less brittle to 
	change parts of the code that return this class 
	'''
	def __init__(self):
		self.tiles = []
		self.coords = []
	
	def add_tile(self, tile, coord):
		self.tiles.append(tile)
		self.coords.append(coord)
	
	def get_tiles_and_coords(self):
		return self.tiles, self.coords

class Loader:
	''' shared tools that can be used by any class that loads from a tileset image '''
	def __init__(self, tilesetImage, gameGridSize):
		# useful local constants
		self.gameGridSize = gameGridSize # the grid_size we are using for display
		self.image = tilesetImage
		self.tileSetGridSize = 24 # each of the square tiles on the image are 24 pixels wide
		self.border = 1 # there is a 1 pixel border around each of the individual square tiles in the image. This border is shared (so the right border of one tile is the left border of the adjacent tile)
		self.scaleFactor = self.tileSetGridSize + self.border # so to jump to the next tile, you need to move the tile width (tileSetGridSize) + the size of the shared border (border)

	def _get_n_by_m_tile_matrix(self, leftX, topY, tileCountInRow, tileCountInColumn):

		# ignores the border on the left and top
		startX = leftX + self.border
		startY = topY + self.border

		tiles, coordinates = [], []

		# example, get 3x3 -> range to startY + 3*scaleFactor because we are grabbing 3 squares starting from startY
		for yDim in range(startY, startY + tileCountInColumn*self.scaleFactor, self.scaleFactor):
			for xDim in range(startX, startX + tileCountInRow*self.scaleFactor, self.scaleFactor):
				tile = self._crop_and_resize_square_image(xDim, yDim)
				tiles.append(tile)
				coordinates.append((xDim, yDim))

		return tiles, coordinates

	def _crop_and_resize_square_image(self, leftX, topY):
		# crop image
		rightX = leftX + self.tileSetGridSize
		bottomY = topY + self.tileSetGridSize
		box = (leftX, topY, rightX, bottomY)
		cropped = self.image.crop(box)

		# resize cropped image
		desiredSize = (self.gameGridSize, self.gameGridSize)
		resized = cropped.resize(desiredSize)
		return resized

from enum import Enum
class TileSimilarity(Enum):
	Different = 0
	Same = 1

class Colors(Enum):
	TEAL=(0, 128, 128)
	BLACK=(1, 1, 1)
	WHITE=(254, 254, 254)

class TemplateTileEmpty(Exception):
	pass

Different = TileSimilarity.Different
Same = TileSimilarity.Same

class TemplateLoader(Loader):
	def __init__(self, tilesetImage, gameGridSize):
		super().__init__(tilesetImage, gameGridSize)

		#we don't want to resize the tiles to fit the grid when loading the template
		# XXX the fact that we have to blindly do this feels like bad design. Make 
		# the _get_n_by_n_tile_matrix() function take a resize factor and then you 
		# won't have to overwrite this here
		self.gameGridSize = self.tileSetGridSize

	def parse_template_column(self):
		# XXX these could likely be member variables
		top = 162
		left = 8

		positionKeyMap = {}

		# get template column (3x24)
		tileCountInRow = 3
		tileCountInColumn = 24
		tiles, coords = self._get_n_by_m_tile_matrix(left, top, tileCountInRow, tileCountInColumn)
		for tile, pos in zip(tiles, coords):
			try:
				threeByThreeMatrixKey = self._calculate_three_by_three_matrix_template_key(tile)
				positionKeyMap[pos] = threeByThreeMatrixKey

			except TemplateTileEmpty:
				print("tile was empty!!")
				# the template doesn't have any information for this tile (it's not in the tileset)

		return positionKeyMap
	'''
exampleKey = (
  (Different, Different, Different),
  (Same,      Same,      Different),
  (Same,      Same,      Different)
)
	'''
	def _calculate_three_by_three_matrix_template_key(self, tile):
		tileColorMatrix = self._get_tile_color_three_by_three_matrix(tile)

		# If center tile in 3x3 2d array is not white, raise TemplateTileEmpty.
		# This is because this tile in the template is unused by the image file.
		if tileColorMatrix[1][1] != Colors.WHITE.value:
			raise TemplateTileEmpty

		threeByThreeMatrixKey = self._turn_color_matrix_into_key(tileColorMatrix)
		return threeByThreeMatrixKey

	def _turn_color_matrix_into_key(self, tileColorMatrix):
		threeByThreeMatrixKey = []
		for row in tileColorMatrix:
			outRow = []
			for color in row:
				# if the space was different from the center space in the template, it will be teal
				if color == Colors.TEAL.value:
					outRow.append(Different)
				else:
					outRow.append(Same)
			threeByThreeMatrixKey.append(tuple(outRow))
		
		return tuple(threeByThreeMatrixKey)

	# works for any "n", but only used for three by three calculations
	# processing a tile in the template to generate a key for fast fetching later
	def _get_tile_color_three_by_three_matrix(self, tile):
		tileCountInRow=3

		rgbTile = tile.convert('RGB')

		innerTemplateTileSize = int(self.tileSetGridSize / tileCountInRow)
		firstInnerTileCenter = int(innerTemplateTileSize - 0.5 * innerTemplateTileSize)
		scaleFactor = innerTemplateTileSize # jump this many pixels to get to the center of the next tile

		tileColorMatrix = []
		# example, get 3x3 -> range to startY + 3*scaleFactor because we are grabbing 3 squares starting from startY
		xCenters = range(firstInnerTileCenter, firstInnerTileCenter + tileCountInRow*scaleFactor, scaleFactor)
		yCenters = range(firstInnerTileCenter, firstInnerTileCenter + tileCountInRow*scaleFactor, scaleFactor)
		for yDim in yCenters:
			row = []
			for xDim in xCenters:
				rgbValue = rgbTile.getpixel((xDim, yDim))
				row.append(rgbValue)
			tileColorMatrix.append(row)
		
		return tileColorMatrix


# images are not hashable because they are mutable, so this is my solution that allows a hashmap
# to index an array of tiles instead
class TileLoader(Loader):
	def __init__(self, tilesetImage, gameGridSize, tileTypeToColumnNumberAssignments, templateLoader):
		super().__init__(tilesetImage, gameGridSize)
		# data structure
		self.tiles = []
		self.tileIndex = {} # string -> index_to_tiles_array

		self.templateLoader = templateLoader

		# perform load of the tileset into the data structures
		self._populate_data(tileTypeToColumnNumberAssignments)

	def get_tile(self, tileType, tileNeighborSettings):
		arrayIndex = self.tileIndex[tileType][tileNeighborSettings]
		return self.tiles[arrayIndex]

	# perform load of the tileset into the data structures
	def _populate_data(self, tileTypeToColumnNumberAssignments):

		# key: value mapping where the key is the arrangement of columns as discussed 
		# here: https://github.com/modelarious/DungeonWalker/issues/64#issuecomment-660400003
		templateColumn = self._parse_template_column()
		
		# populate the requested tile types from the requested columns
		for tileType, columnNumber in tileTypeToColumnNumberAssignments.items():
			self.tileIndex[tileType] = {}
			self._populate_from_column(tileType, columnNumber, templateColumn)
		
		# XXX just display the whole thing
		# for tileType, tileDictionary in self.tileIndex.items():
		# 	for tile in self.tileIndex[tileType].values():
		# 		tile.show()
		# 	input()
	
	def _add_tile(self, tileType, tile, tileNeighborSettings):
		self.tileIndex[tileType][tileNeighborSettings] = len(self.tiles)
		self.tiles.append(self._export_for_pygame(tile))

	# translate from PIL to pygame so the tile can be drawn to the screen
	def _export_for_pygame(self, tile):
		strFormat = 'RGBA'
		# https://riptutorial.com/pygame/example/21220/using-with-pil fetched on July 13, 2020
		rawBytesTile = tile.tobytes("raw", strFormat)
		pygameTile = pygame.image.fromstring(rawBytesTile, tile.size, strFormat)
		return pygameTile
	
	def _parse_template_column(self):
		return self.templateLoader.parse_template_column()

	# fetches the legend from the file
	def _populate_from_column(self, tileType, columnNumber, templateColumn):

		# move to the requested column. * 3 because the scaleFactor applies to 
		# single tiles and we need to jump over 3 of them to get to the next column.
		# therefore we need to jump over 3 * columnNumber to get to columnNumber
		scaling = self.scaleFactor * 3 * columnNumber

		# pull out all the tiles that we found in the template, but from the current column instead, 
		# and use the key created when building the template in order to store them. For more 
		# info, see here: https://github.com/modelarious/DungeonWalker/issues/64#issuecomment-660400003
		for tileOffset, threeByThreeMatrixKey in templateColumn.items():
			x, y = tileOffset
			thisColX = x + scaling
			tile = self._crop_and_resize_square_image(thisColX, y)
			self._add_tile(tileType, tile, threeByThreeMatrixKey)


			