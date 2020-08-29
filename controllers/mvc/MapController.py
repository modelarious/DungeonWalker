from controllers.mvc.ControllerBaseClass import ControllerBaseClass

class MapController(ControllerBaseClass):
	def __init__(self, mapModel, mapView, mapModelFactory, tileMapper):
		self._mapModel = mapModel
		self._mapView = mapView
		self._mapModelFactory = mapModelFactory
		self._tileMapper = tileMapper

		# will be populated by a call to register_enemy_orchestrator. Then this controller
		# will notify the enemyOrchestrator when it is time to generate new spawn points.
		# XXX future: this might become array when there are multiple enemy types
		self.enemyOrchestrator = None
	
	# XXX these are obviously really bad signs of an ownership problem.
	# XXX anyone using these functions should instead own the mapModel and just ask it directly
	def get_map(self):
		return self._mapModel.get_board()
	
	def get_starting_coordinates(self):
		return self._mapModel.get_starting_coordinates()
	
	def get_goal_space_coords(self):
		return self._mapModel.get_goal_space_coords()
	
	def get_enemy_spawn_points(self):
		return self._mapModel.get_spawn_points()
	
	# XXX I'd say the below 3 functions are all that should make up the mapController
	def updateView(self, game_screen):
		# here I made the view inspect the model directly, though some sources say that I should be
		# getting the data out in the controller and then passing it to the view
		self._mapView.updateView(game_screen, self._mapModel)
	
	def generate_new_map(self):
		self._mapModel = self._mapModelFactory.generate_new_map()
		if self.enemyOrchestrator:
			print("generate new enemies")
			self.enemyOrchestrator.generate_new_enemies()
		self._tileMapper.process_board(self._mapModel)
	
	# due to the order of construction of objects, the enemyOrchestrator uses the observer pattern
	# to know when to update itself
	def register_enemy_orchestrator(self, enemyOrchestrator):
		self.enemyOrchestrator = enemyOrchestrator
