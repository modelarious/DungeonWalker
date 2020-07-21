import pygame
from TileMapping.TileLoading.LoaderBaseClass import LoaderBaseClass
from TileMapping.TileLoading.KeyMapping import map_key_that_doesnt_exist_in_tileset_to_one_that_does


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
