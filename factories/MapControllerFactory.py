from views.MapView import MapView
from controllers.mvc.MapController import MapController
from MapGenerationDrivers.RandomMapGenerationDriver import RandomMapGenerationDriver
from factories.FactoryBaseClass import FactoryBaseClass
from factories.MapModelFactory import MapModelFactory

from TileMapping.TileMapper import TileMapper
from TileMapping.TileMapper import TileLoader
from TileMapping.TileLoader import TemplateLoader
from PIL import Image
from TileMapping.TileType import TileType
from views.TileMappedView import TileMappedView

class MapControllerFactory(FactoryBaseClass):
	def __init__(self, max_x_tiles, max_y_tiles, grid_size):
		self.max_x_tiles = max_x_tiles
		self.max_y_tiles = max_y_tiles
		self._grid_size = grid_size
	
	def getController(self):

		# XXX RandomMapGenerationDriver instantiation is weird, should make it so 
		# that you pass in RandomMapGenerationDriver(), then register the map with it
		mapModelFactory = MapModelFactory(
			self.max_x_tiles, 
			self.max_y_tiles, 
			RandomMapGenerationDriver
		)
		mapModel = mapModelFactory.generate_new_map()

		# XXX this is a lot of baggage for one factory
		# and a lot is related to tile mapping, so make that into a separate factory
		infile2 = "assets/tilesets/test_dungeon.png"
		with Image.open(infile2) as im:

			# this could be changed to an array of objects that contain a tileType and a column number
			tileTypeToColumnNumberAssignments = {
				TileType.WALL: 1,
				TileType.GROUND: 3
			}
			templateLoader = TemplateLoader(im, self._grid_size)
			tileLoader = TileLoader(im, self._grid_size, tileTypeToColumnNumberAssignments, templateLoader)

		tileMapper = TileMapper(tileLoader)
		tileMapper.process_board(mapModel)
		tileMapperView = TileMappedView(self._grid_size, tileMapper)

		mapView = MapView(self._grid_size, tileMapperView)

		return MapController(mapModel, mapView, mapModelFactory, tileMapper)

