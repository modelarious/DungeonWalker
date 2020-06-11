from views.MapView import MapView
from controllers.mvc.MapController import MapController
from MapGenerators.RandomMapControllerGenerator import RandomMapControllerGenerator
from factories.FactoryBaseClass import FactoryBaseClass
from factories.MapModelFactory import MapModelFactory

class MapControllerFactory(FactoryBaseClass):
	def __init__(self, max_x_tiles, max_y_tiles):
		self.max_x_tiles = max_x_tiles
		self.max_y_tiles = max_y_tiles
	
	def getController(self):
		
		mapModel = MapModelFactory(
			self.get_copy(self.max_x_tiles), 
			self.get_copy(self.max_y_tiles), 
			RandomMapControllerGenerator
		).getMapModel()

		mapView = MapView()
		return MapController(mapModel, mapView)

