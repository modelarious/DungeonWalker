from controllers.mvc.ControllerBaseClass import ControllerBaseClass

class MapController(ControllerBaseClass):
	def __init__(self, mapModel, mapView):
		self.mapModel = mapModel
		self.mapView = mapView
	
	def updateView(self, game_screen):
		# here I made the view inspect the model directly, though some sources say that I should be
		# getting the data out in the controller and then passing it to the view
		self.mapView.updateView(game_screen, self.mapModel)
