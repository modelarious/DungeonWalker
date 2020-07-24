from TileMapping.TileMapper import TileMapper
from TileMapping.TileLoading.LegendLoader import LegendLoader
from TileMapping.TileLoading.TileLoader import TileLoader
from TileMapping.TileType import TileType
from TileMapping.TileLoading.StairLoader import StairLoader
from views.TileMappedView import TileMappedView
from PIL import Image
from random import choice

class RandomTileMapperFactory:
	def __init__(self, gridSize, mapModel):
		self.gridSize = gridSize
		self.mapModel = mapModel

	def get_tile_mapper_and_view(self):
		# randomize the input file
		# XXX turn these into classes!!!
		tilesets = [
			[
				"assets/tilesets/test_dungeon.png",
				# XXX this could be changed to an array of objects that contain a tileType and a column number
				{
					TileType.WALL: 1,
					TileType.GROUND: 3
				}
			],
			[
				"assets/tilesets/world abyss.png",
				{
					TileType.WALL: 1,
					TileType.GROUND: 4
				}
			],
			[
				"assets/tilesets/Deep Dark Crater.png",
				{
					TileType.WALL: 1,
					TileType.GROUND: 7
				}
			]
		]
		infile, tileTypeToColumnNumberAssignments = choice(tilesets)

		# XXX might be nice to encapsulate the next three lines in another factory
		with Image.open(infile) as im:
			legendLoader = LegendLoader(im, self.gridSize)
			tileLoader = TileLoader(im, self.gridSize, tileTypeToColumnNumberAssignments, legendLoader)

		stairsFile = "assets/tilesets/stairs.png"
		with Image.open(stairsFile) as im:
			stairLoader = StairLoader(im, self.gridSize)
			stairLoader.process_stairs() # XXX should probably happen on init, because you need to load data while the image file is open 
			#XXX maybe rethink how these classes use their image files.... not great that they can only use them when they're open here

		tileMapper = TileMapper(tileLoader, stairLoader)
		tileMapper.process_board(self.mapModel)
		tileMapperView = TileMappedView(self.gridSize, tileMapper)
		return tileMapper, tileMapperView