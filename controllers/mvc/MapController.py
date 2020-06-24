from controllers.mvc.ControllerBaseClass import ControllerBaseClass

class MapController(ControllerBaseClass):
	def __init__(self, mapModel, mapView):
		self._mapModel = mapModel
		self._mapView = mapView
	
	def get_map(self):
		return self._mapModel.get_board()
	
	def place_player_at_starting_location(self):
		self._mapModel.set_start_tile

	
	def updateView(self, game_screen):
		# here I made the view inspect the model directly, though some sources say that I should be
		# getting the data out in the controller and then passing it to the view
		self._mapView.updateView(game_screen, self._mapModel)
