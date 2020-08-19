from views.MapView import MapView
from controllers.mvc.MapController import MapController
from MapGenerationDrivers.RandomMapGenerationDriver import RandomMapGenerationDriver
from factories.FactoryBaseClass import FactoryBaseClass
from factories.MapModelFactory import MapModelFactory
from factories.RandomTileMapperFactory import RandomTileMapperFactory

class MapControllerMapModelFactory(FactoryBaseClass):
	def __init__(self, max_x_tiles, max_y_tiles, grid_size, tileMapperFactoryClass=RandomTileMapperFactory):
		self.max_x_tiles = max_x_tiles
		self.max_y_tiles = max_y_tiles
		self._grid_size = grid_size # XXX why is this hidden... be consistent
		self.tileMapperFactoryClass = tileMapperFactoryClass
	
	def getController(self):

		# XXX RandomMapGenerationDriver instantiation is weird, should make it so 
		# that you pass in RandomMapGenerationDriver(), then register the map with it
		mapModelFactory = MapModelFactory(
			self.max_x_tiles, 
			self.max_y_tiles, 
			RandomMapGenerationDriver
		)
		mapModel = mapModelFactory.generate_new_map()

		# XXX need to decide how to do this, should I be passing 
		# in the RandomTileMapperFactory class pointer?
		tileMapper, tileMapperView = self.tileMapperFactoryClass(
			self._grid_size, 
			mapModel
		).get_tile_mapper_and_view()
		
		mapView = MapView(self._grid_size, tileMapperView)

		return MapController(mapModel, mapView, mapModelFactory, tileMapper), mapModel