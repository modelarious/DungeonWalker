from views.MapView import MapView
from controllers.mvc.MapController import MapController
from MapGenerationDrivers.RandomMapGenerationDriver import RandomMapGenerationDriver
from factories.FactoryBaseClass import FactoryBaseClass
from factories.MapModelFactory import MapModelFactory

from TileMapping.TileMapper import TileMapper
from TileMapping.TileMapper import TileLoader
from PIL import Image
from TileMapping.TileType import TileType

class MapControllerFactory(FactoryBaseClass):
	def __init__(self, max_x_tiles, max_y_tiles, grid_size):
		self.max_x_tiles = max_x_tiles
		self.max_y_tiles = max_y_tiles
		self._grid_size = grid_size
	
	def getController(self):

		# XXX RandomMapGenerationDriver instantiation is weird, should make it so 
		# that you pass in RandomMapGenerationDriver(), then register the map with it
		mapModelFactory = MapModelFactory(
			self.get_copy(self.max_x_tiles), 
			self.get_copy(self.max_y_tiles), 
			RandomMapGenerationDriver
		)
		mapModel = mapModelFactory.generate_new_map()

		mapView = MapView(self.get_copy(self._grid_size))

		# XXX this is a lot of baggage for one factory
		# and a lot is related to tile mapping, so make that into a separate factory
		tileLoader = None
		infile2 = "assets/tilesets/world abyss.png"
		with Image.open(infile2) as i:
			tileTypeToColumnNumberAssignments = {
				TileType.WALL: 1,
				TileType.GROUND: 4
			}
			tileLoader = TileLoader(i, tileTypeToColumnNumberAssignments)

		tileMapper = TileMapper(mapModel, tileLoader)

		return MapController(mapModel, mapView, mapModelFactory, tileMapper)

