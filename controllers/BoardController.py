from controllers.ControllerBaseClass import ControllerBaseClass

class BoardController(ControllerBaseClass):
	def __init__(self, boardModel, boardView):
		self.boardModel = boardModel
		self.boardView = boardView
	
	def updateView(self, game_screen):
		# here I made the view inspect the model directly, though some sources say that I should be
		# getting the data out in the controller and then passing it to the view
		self.boardView.updateView(game_screen, self.boardModel)
	
	def getGameDimensions(self):
		return self.boardModel.game_dimensions
