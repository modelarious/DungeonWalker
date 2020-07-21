from TileMapping.TileLoading.LoaderBaseClass import LoaderBaseClass
from TileMapping.TileLoading.TileSimilarity import Same, Different
from TileMapping.TileLoading.LegendTileColors import Colors
from exceptions import LegendTileEmpty

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