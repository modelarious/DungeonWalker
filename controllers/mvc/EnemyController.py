from controllers.mvc.CharacterController import CharacterController

from helpers.Direction import Left, Right, Up, Down, NullMove

from random import shuffle
from helpers.ManhattenDistance import manhatten_distance

# type hints
from controllers.mvc.MapController import MapController
from models.CharacterModel import CharacterModel
from views.CharacterView import CharacterView
from controllers.mvc.PlayerController import PlayerController

class AIUnit:
	def __init__(self):
		self.blah = 0
	

class FivePlyLookaheadAIUnit(AIUnit):
	def __init__(self):
		self.bleh = 3



# XXX might be better not to give the enemy controller the player controller but instead an object that
# wraps the player model and lets the enemy make queries about the player 
class EnemyController(CharacterController):
	def __init__(self, 
			characterView: CharacterView,
			characterModel: CharacterModel,
			mapController: MapController,
			playerController: PlayerController ):
		super().__init__(characterView, characterModel, mapController)
		self.playerController = playerController

	def update_position(self, preventedPositions):
		directions = [Right(), Left(), Up(), Down(), NullMove()]
		shuffle(directions)


		# XXX STATE PATTERN PLEEEEEEASE
		# if the enemy is far away from the player, just move randomly
		playerPosition = self.playerController.get_pos()
		if manhatten_distance(*playerPosition, *self._characterModel.get_pos()) > 7:
			for move in directions:
				if self.movement_valid(move) and not self.movement_prevented(move, preventedPositions):
					self._characterModel.move(move)
					return True

			# didn't find a move that worked
			return False

		# keep track of the minimum distance to the player
		# pick the move that gets the enemy closest
		infinity = 999999999
		minDistToPlayer = infinity
		selectedMovement = None
		for move in directions:
			if self.movement_valid(move) and not self.movement_prevented(move, preventedPositions):
				distToPlayer = manhatten_distance(*playerPosition, *self._characterModel.get_speculative_position(move))
				if distToPlayer < minDistToPlayer:
					minDistToPlayer = distToPlayer
					selectedMovement = move

		if selectedMovement == None:
			return False
		
		self._characterModel.move(selectedMovement)
		return True