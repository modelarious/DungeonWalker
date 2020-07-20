from TileMapping.TileMapper import TileMapper
from TileMapping.TileLoader import TemplateLoader, TileLoader
from TileMapping.TileType import TileType
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
			templateLoader = TemplateLoader(im, self.gridSize)
			tileLoader = TileLoader(im, self.gridSize, tileTypeToColumnNumberAssignments, templateLoader)

		tileMapper = TileMapper(tileLoader)
		tileMapper.process_board(self.mapModel)
		tileMapperView = TileMappedView(self.gridSize, tileMapper)
		return tileMapper, tileMapperView