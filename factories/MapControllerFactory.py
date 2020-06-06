from models.MapModel import MapModel
from views.MapView import MapView
from controllers.MapController import MapController
from helpers.Autoconnect import Autoconnect

class MapControllerFactory():
	def __init__(self, max_x_grid_spaces, max_y_grid_spaces):
		self.max_x_grid_spaces = max_x_grid_spaces
		self.max_y_grid_spaces = max_y_grid_spaces
	
	def getController(self):
		autoconnect = Autoconnect()
		mapModel = MapModel(self.max_x_grid_spaces, self.max_y_grid_spaces, autoconnect)
		mapView = MapView()
		return MapController(mapModel, mapView)

