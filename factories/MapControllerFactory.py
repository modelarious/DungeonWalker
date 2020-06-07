from models.MapModel import MapModel
from views.MapView import MapView
from controllers.mvc.MapController import MapController
from helpers.Autoconnect import Autoconnect
from MapGenerators.RandomMapGenerator import RandomMapGenerator
from factories.FactoryBaseClass import FactoryBaseClass
from factories.MapModelFactory import MapModelFactory

class MapControllerFactory(FactoryBaseClass):
	def __init__(self, max_x_grid_spaces, max_y_grid_spaces):
		self.max_x_grid_spaces = max_x_grid_spaces
		self.max_y_grid_spaces = max_y_grid_spaces
	
	def getController(self):
		autoconnect = Autoconnect()
		mapModel = MapModelFactory(self.max_x_grid_spaces, self.max_y_grid_spaces, autoconnect, RandomMapGenerator).getMapModel()
		mapView = MapView()
		return MapController(mapModel, mapView)

