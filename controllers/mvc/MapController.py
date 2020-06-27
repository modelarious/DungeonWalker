from controllers.mvc.ControllerBaseClass import ControllerBaseClass

class MapController(ControllerBaseClass):
	def __init__(self, mapModel, mapView, mapModelFactory):
		self._mapModel = mapModel
		self._mapView = mapView
		self._mapModelFactory = mapModelFactory
	
	def get_map(self):
		return self._mapModel.get_board()
	
	def get_starting_coordinates(self):
		return self._mapModel.get_starting_coordinates()
	
	def get_goal_space_coords(self):
		return self._mapModel.get_goal_space_coords()
	
	def updateView(self, game_screen):
		# here I made the view inspect the model directly, though some sources say that I should be
		# getting the data out in the controller and then passing it to the view
		self._mapView.updateView(game_screen, self._mapModel)
	
	def is_legal_move(self, start_pos, prospective_pos):
		return self._mapModel.is_legal_move(start_pos, prospective_pos)
	
	def generate_new_map(self):
		self._mapModel = self._mapModelFactory.generate_new_map()
