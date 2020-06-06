from controllers.ControllerBaseClass import ControllerBaseClass

class GridController(ControllerBaseClass):
	def __init__(self, gridModel, gridView):
		self.gridModel = gridModel
		self.gridView = gridView
	
	def updateView(self, game_screen):
		# here I made the view inspect the model directly, though some sources say that I should be
		# getting the data out in the controller and then passing it to the view
		self.gridView.updateView(game_screen, self.gridModel)
	
	def getGameDimensions(self):
		return self.gridModel.game_dimensions
