from models.MapModel import MapModel
from views.MapView import MapView
from controllers.mvc.MapController import MapController
from helpers.Autoconnect import Autoconnect
from MapGenerators.RandomMapGenerator import RandomMapGenerator

class MapControllerFactory():
	def __init__(self, max_x_grid_spaces, max_y_grid_spaces):
		self.max_x_grid_spaces = max_x_grid_spaces
		self.max_y_grid_spaces = max_y_grid_spaces
	
	def getController(self):
		autoconnect = Autoconnect()
		mapModel = MapModel(self.max_x_grid_spaces, self.max_y_grid_spaces, autoconnect)
		mapView = MapView()
		mapGenerator = RandomMapGenerator(mapModel)
		return MapController(mapGenerator, mapView)

