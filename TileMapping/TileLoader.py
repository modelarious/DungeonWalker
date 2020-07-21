from TileMapping.TileType import TileType
import pygame
from PIL import Image

class LoaderBaseClass:
	''' shared tools that can be used by any class that loads from a tileset image '''
	def __init__(self, tilesetImage, gameGridSize):
		# useful local constants
		self.gameGridSize = gameGridSize # the grid_size we are using for display
		self.image = tilesetImage
		self.tileSetGridSize = 24 # each of the square tiles on the image are 24 pixels wide
		self.border = 1 # there is a 1 pixel border around each of the individual square tiles in the image. This border is shared (so the right border of one tile is the left border of the adjacent tile)
		self.scaleFactor = self.tileSetGridSize + self.border # so to jump to the next tile, you need to move the tile width (tileSetGridSize) + the size of the shared border (border)

	def _get_n_by_m_tile_matrix(self, leftX, topY, tileCountInRow, tileCountInColumn, resizeFactor):

		# ignores the border on the left and top
		startX = leftX + self.border
		startY = topY + self.border

		tiles, coordinates = [], []

		# example, get 3x3 -> range to startY + 3*scaleFactor because we are grabbing 3 squares starting from startY
		for yDim in range(startY, startY + tileCountInColumn*self.scaleFactor, self.scaleFactor):
			for xDim in range(startX, startX + tileCountInRow*self.scaleFactor, self.scaleFactor):
				tile = self._crop_and_resize_square_image(xDim, yDim, resizeFactor)
				tiles.append(tile)
				coordinates.append((xDim, yDim))

		return tiles, coordinates

	def _crop_and_resize_square_image(self, leftX, topY, resizeFactor):
		# crop image
		rightX = leftX + self.tileSetGridSize
		bottomY = topY + self.tileSetGridSize
		box = (leftX, topY, rightX, bottomY)
		cropped = self.image.crop(box)

		# resize cropped image
		resized = cropped.resize(resizeFactor)
		return resized

from enum import Enum
class TileSimilarity(Enum):
	Different = 0
	Same = 1

class Colors(Enum):
	TEAL=(0, 128, 128)
	BLACK=(1, 1, 1)
	WHITE=(254, 254, 254)

class LegendTileEmpty(Exception):
	pass

Different = TileSimilarity.Different
Same = TileSimilarity.Same

class LegendLoader(LoaderBaseClass):
	def parse_legend_column(self):
		# Starting pixel of the tiles in the legend.
		# Same for all pokemon tileset image files
		top = 162
		left = 8

		# get legend column (3x24)
		tileCountInRow = 3
		tileCountInColumn = 24

		# data structure (x, y) -> 3x3 matrix of TileSimilarity
		'''
		exampleKey = (
  			(Different, Different, Different),
  			(Same,      Same,      Different),
  			(Same,      Same,      Different)
		)
		'''
		# you can add an offset to the (x, y) to grab a related tile from another column
		# and the key will allow us to map the mapModel to the pokemon tiles
		positionKeyMap = {}

		# no resize.  This is the original gridsize of the image we are loading from
		resizeFactor = (self.tileSetGridSize, self.tileSetGridSize)
		tiles, coords = self._get_n_by_m_tile_matrix(left, top, tileCountInRow, tileCountInColumn, resizeFactor)
		for tile, pos in zip(tiles, coords):
			try:
				threeByThreeMatrixKey = self._calculate_three_by_three_matrix_legend_key(tile)
				positionKeyMap[pos] = threeByThreeMatrixKey

			except LegendTileEmpty:
				pass
				# the legend doesn't have any information for this tile (this position is not in the tileset)

		return positionKeyMap
	'''
exampleKey = (
  (Different, Different, Different),
  (Same,      Same,      Different),
  (Same,      Same,      Different)
)
	'''
	def _calculate_three_by_three_matrix_legend_key(self, tile):
		tileColorMatrix = self._get_tile_color_three_by_three_matrix(tile)

		# If center tile in 3x3 2d array is not white, raise LegendTileEmpty.
		# This is because this tile in the legend is unused by the image file.
		if tileColorMatrix[1][1] != Colors.WHITE.value:
			raise LegendTileEmpty

		threeByThreeMatrixKey = self._turn_color_matrix_into_key(tileColorMatrix)
		return threeByThreeMatrixKey

	# XXX consider doing the get_tile_color and this step all in one (ie get tileColor, map it to Different or Same)
	# XXX raise an exception if tileColorMatrix[1][1] != Colors.WHITE.value
	def _turn_color_matrix_into_key(self, tileColorMatrix):
		threeByThreeMatrixKey = []
		for row in tileColorMatrix:
			outRow = []
			for color in row:
				# if the space was different from the center space in the legend, it will be teal
				if color == Colors.TEAL.value:
					outRow.append(Different)
				else:
					outRow.append(Same)
			threeByThreeMatrixKey.append(tuple(outRow))
		
		return tuple(threeByThreeMatrixKey)

	# works for any "n", but only used for three by three calculations
	# processing a tile in the legend to generate a key for fast fetching later
	def _get_tile_color_three_by_three_matrix(self, tile):
		tileCountInRow=3

		rgbTile = tile.convert('RGB')

		innerLegendTileSize = int(self.tileSetGridSize / tileCountInRow)
		firstInnerTileCenter = int(innerLegendTileSize - 0.5 * innerLegendTileSize)
		scaleFactor = innerLegendTileSize # jump this many pixels to get to the center of the next tile

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
class TileLoader(LoaderBaseClass):
	def __init__(self, tilesetImage, gameGridSize, tileTypeToColumnNumberAssignments, legendLoader):
		super().__init__(tilesetImage, gameGridSize)
		# data structure
		self.tiles = []
		self.tileIndex = {} # string -> index_to_tiles_array

		self.legendLoader = legendLoader

		# perform load of the tileset into the data structures
		self._populate_data(tileTypeToColumnNumberAssignments)

	def get_tile(self, tileType, tileNeighborSettings):
		# there are 512 arrangement of 9 spaces with 2 choices for each space
		# (512 arrangements of Same and Different into a 3x3 grid)
		# but there are only ~40 tiles in the legend. This means 
		# we need to remap some keys that don't exist in our 
		# tileset to ones that do.
		processedTileNeighborSettings = self._possibly_remap_incoming_key_to_actual_tile(tileType, tileNeighborSettings)
		arrayIndex = self.tileIndex[tileType][processedTileNeighborSettings]
		return self.tiles[arrayIndex]
	
	def _possibly_remap_incoming_key_to_actual_tile(self, tileType, tileNeighborSettings):
		# there are 512 arrangement of 9 spaces with 2 choices for each space
		# (512 arrangements of Same and Different into a 3x3 grid)
		# but there are only ~40 tiles in the legend. This means 
		# we need to remap some keys that don't exist in our 
		# tileset to ones that do.

		# if the arrangement exists in our tileset, just use that
		if tileNeighborSettings in self.tileIndex[tileType]:
			return tileNeighborSettings
		
		# else defer to mapping function to update the key to one that exists in the tileset
		# and will fill the correct role
		return map_key_that_doesnt_exist_in_tileset_to_one_that_does(tileNeighborSettings)

	# perform load of the tileset into the data structures
	def _populate_data(self, tileTypeToColumnNumberAssignments):

		# key: value mapping where the key is the arrangement of columns as discussed 
		# here: https://github.com/modelarious/DungeonWalker/issues/64#issuecomment-660400003
		legendColumn = self._parse_legend_column()
		
		# populate the requested tile types from the requested columns
		for tileType, columnNumber in tileTypeToColumnNumberAssignments.items():
			self.tileIndex[tileType] = {}
			self._populate_from_column(tileType, columnNumber, legendColumn)
	
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
	
	def _parse_legend_column(self):
		return self.legendLoader.parse_legend_column()

	# fetches the legend from the file
	def _populate_from_column(self, tileType, columnNumber, legendColumn):

		# move to the requested column. * 3 because the scaleFactor applies to 
		# single tiles and we need to jump over 3 of them to get to the next column.
		# therefore we need to jump over 3 * columnNumber to get to columnNumber
		scaling = self.scaleFactor * 3 * columnNumber

		# pull out all the tiles that we found in the legend, but from the current column instead, 
		# and use the key created when building the legend in order to store them. For more 
		# info, see here: https://github.com/modelarious/DungeonWalker/issues/64#issuecomment-660400003
		for tileOffset, threeByThreeMatrixKey in legendColumn.items():
			x, y = tileOffset
			thisColX = x + scaling
			# resize to fit the game grid
			resizeFactor = (self.gameGridSize, self.gameGridSize)
			tile = self._crop_and_resize_square_image(thisColX, y, resizeFactor)
			self._add_tile(tileType, tile, threeByThreeMatrixKey)





def map_key_that_doesnt_exist_in_tileset_to_one_that_does(tileNeighborSettings):
	upperNeighbor = tileNeighborSettings[0][1]
	lowerNeighbor = tileNeighborSettings[2][1]
	leftNeighbor  = tileNeighborSettings[1][0]
	rightNeighbor = tileNeighborSettings[1][2]

	# build-a-key
	# if right neighbor is different, make all right tiles Different
	# if bottom neighbor is different, make all bottom tiles Different
	# etc...
	buildAKey = [
		[Same, Same, Same],
		[Same, Same, Same],
		[Same, Same, Same]
	]

	#apply all 4 of the following tests to map to a tile in the dataset
	if rightNeighbor == Different:
		# set the right side to Different
		# ex:
		# 	correctedKey = (
  		# 		(Same, Same, Different),
  		# 		(Same, Same, Different),
  		# 		(Same, Same, Different)
		# 	)
		for row in range(len(buildAKey)):
			buildAKey[row][-1] = Different
	
	if leftNeighbor == Different:
		# set the left side to Different
		# ex:
		# 	correctedKey = (
  		# 		(Different, Same, Same),
  		# 		(Different, Same, Same),
  		# 		(Different, Same, Same)
		# 	)
		for row in range(len(buildAKey)):
			buildAKey[row][0] = Different
	
	if lowerNeighbor == Different:
		# set the bottom row side to Different
		# ex:
		# 	correctedKey = (
  		# 		(Same, Same, Same),
  		# 		(Same, Same, Same),
  		# 		(Different, Different, Different)
		# 	)
		buildAKey[-1] = [Different, Different, Different]
	
	if upperNeighbor == Different:
		# set the top row side to Different
		# ex:
		# 	correctedKey = (
  		# 		(Same, Same, Same),
  		# 		(Same, Same, Same),
  		# 		(Different, Different, Different)
		# 	)
		buildAKey[0] = [Different, Different, Different]

	# turn our 3x3 array into 3x3 tuple so it is hashable
	tupleCorrectedKey = []
	for row in buildAKey:
		tupleCorrectedKey.append(tuple(row))

	return tuple(tupleCorrectedKey)

