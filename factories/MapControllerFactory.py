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

		#XXX this is ripe for refactor. Most methods in mapModel are used once when creating
		# the board, so these steps could likely be captured elsewhere 
		# (perhaps MapGeneratorBaseClass). and it wouldn't need the autoconnect unit
		mapGenerator = RandomMapGenerator(mapModel)
		return MapController(mapGenerator, mapView)

