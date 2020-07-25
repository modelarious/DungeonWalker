from controllers.mvc.CharacterController import CharacterController

from helpers.Direction import Left, Right, Up, Down, NullMove

from random import shuffle
from helpers.ManhattenDistance import manhatten_distance

# type hints
from controllers.mvc.MapController import MapController
from models.CharacterModel import CharacterModel
from views.CharacterView import CharacterView
from controllers.mvc.PlayerController import PlayerController


# should be abstract class that defines an interface
class AIState:
	def __init__(self, playerModel, enemyController):
		self.playerController = playerModel
		self.enemyController = enemyController
		self.lookahead = 7
	
	def decide_on_movement(self, directions, preventedPositions):
		pass

	def player_within_range(self):
		# consider transitioning to attack state if in range of player
		N = self.lookahead
		playerPosition = self.playerController.get_pos()
		if manhatten_distance(*playerPosition, *self.enemyController.get_pos()) <= N:
			return True
		return False
	
	def movement_allowed(self, move, preventedPositions):
		return self.enemyController.movement_valid(move) and not self.enemyController.movement_prevented(move, preventedPositions)


	

# NOTE: this is not something like minimax, it's not even A*,
# it's brute forcing to find the direction that can put the enemy
# closest to the player in N moves
class NPlyLookaheadAIState(AIState):
	def decide_on_movement(self, directions, preventedPositions):
		# consider transitioning back to random moves if the player is now out of range
		if not self.player_within_range():
			newState = RandomAIState(self.playerController, self.enemyController)
			self.enemyController.update_state(newState)
			return newState.decide_on_movement(directions, preventedPositions)

		# XXX perform lookahead by self.lookahead moves
		return NullMove()

class RandomAIState(AIState):

	def decide_on_movement(self, directions, preventedPositions):
		# consider transitioning to attack state if in range of player
		if self.player_within_range():
			newState = NPlyLookaheadAIState(self.playerController, self.enemyController)
			self.enemyController.update_state(newState)
			return newState.decide_on_movement(directions, preventedPositions)

		# since the enemy is far away from the player, just move randomly
		for move in directions:
			if self.movement_allowed(move, preventedPositions):
				return move

		# didn't find a move that worked
		return None



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

		beginningAIState = RandomAIState(self.playerController, self) # XXX pass this in
		self.AIState = beginningAIState

	def update_position(self, preventedPositions):
		directions = [Right(), Left(), Up(), Down(), NullMove()]
		shuffle(directions)
		move = self.AIState.decide_on_movement(directions, preventedPositions)

		if move == None:
			return False
		
		self._characterModel.move(move)
		return True
	
	def update_state(self, newState):
		self.AIState = newState
		
			

		# # keep track of the minimum distance to the player
		# # pick the move that gets the enemy closest
		# infinity = 999999999
		# minDistToPlayer = infinity
		# selectedMovement = None
		# for move in directions:
		# 	if self.movement_valid(move) and not self.movement_prevented(move, preventedPositions):
		# 		distToPlayer = manhatten_distance(*playerPosition, *self._characterModel.get_speculative_position(move))
		# 		if distToPlayer < minDistToPlayer:
		# 			minDistToPlayer = distToPlayer
		# 			selectedMovement = move

		# if selectedMovement == None:
		# 	return False
		
		# self._characterModel.move(selectedMovement)
		# return True