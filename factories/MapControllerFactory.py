from views.MapView import MapView
from controllers.mvc.MapController import MapController
from MapGenerators.RandomMapGenerationController import RandomMapGenerationController
from factories.FactoryBaseClass import FactoryBaseClass
from factories.MapModelFactory import MapModelFactory

class MapControllerFactory(FactoryBaseClass):
	def __init__(self, max_x_tiles, max_y_tiles, grid_size):
		self.max_x_tiles = max_x_tiles
		self.max_y_tiles = max_y_tiles
		self._grid_size = grid_size
	
	def getController(self):
		mapModel = MapModelFactory(
			self.get_copy(self.max_x_tiles), 
			self.get_copy(self.max_y_tiles), 
			RandomMapGenerationController
		).getMapModel()

		mapView = MapView(self.get_copy(self._grid_size))
		return MapController(mapModel, mapView)

