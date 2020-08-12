from controllers.mvc.CharacterController import CharacterController

from helpers.Direction import Left, Right, Up, Down, NullMove

from random import shuffle
from helpers.ManhattenDistance import manhatten_distance

# type hints
from controllers.mvc.MapController import MapController
from models.CharacterModel import CharacterModel
from views.CharacterView import CharacterView
from controllers.mvc.PlayerController import PlayerController

infinity = 999999999

# should be abstract class that defines an interface
class AIState:
	def __init__(self, playerController, enemyController, enemyModel):
		self.playerController = playerController
		self.enemyController = enemyController
		self.enemyModel = enemyModel
		self.lookahead = 7

	def decide_on_movement(self, directions, preventedPositions):
		pass

	def player_within_range(self):
		# consider transitioning to attack state if in range of player
		N = self.lookahead
		if self.get_distance_to_player() <= N:
			return True
		return False
	
	def get_distance_to_player(self):
		playerPosition = self.playerController.get_pos()
		return manhatten_distance(*playerPosition, *self.enemyModel.get_pos())
	
	def get_speculative_distance_to_player(self, move):
		playerPosition = self.playerController.get_pos()
		return manhatten_distance(*playerPosition, *self.enemyModel.get_speculative_position(move))

	# check if this is a legal move
	# XXX this shouldn't be handled by the controller
	def movement_allowed(self, move, preventedPositions):
		return self.enemyController.movement_valid(move) and not self.enemyController.movement_prevented(move, preventedPositions)
	
	# this is a state in which the 
	# XXX this shouldn't be handled by the controller
	def is_winning_state(self, position):
		# XXX yeah, this is gross, so give this object the model then!
		return self.playerController._characterModel.get_pos() == position

# XXX NOTE: this is not something like minimax, it's not even A*,
# it's brute forcing to find the directions that the enemy can walk that 
# can put them closest to the player in N moves
class NPlyLookaheadAIState(AIState):

	# XXX what happens when you get back up to the top layer? You need to make a decision on what direction to choose
	def depth_limited_recursive_move(self, directions, originalMove, preventedPositions, depth):
		if depth == 0:
			print(f"evaluated distance to be {self.get_distance_to_player()}")
			return self.get_distance_to_player()

		# XXX You're going to need to exclude any search that happens from a node you visited with a shorter path to it already
		# XXX otherwise known as transposition tables -> This would be drastically improved as a bfs as then you
		# XXX would always be filling in the shortest distance to a node when you reach it.  The current
		# XXX dfs approach suffers because you could reach a node for the first time at depth 19, but the 
		# XXX real shortest path is 3 from a different starting move.  Then you will go through the process
		# XXX of updating the shortest distance several times.
		distancesFromPlayer = [infinity]
		for move in directions:
			if self.movement_allowed(move, preventedPositions):
				print("\t"* depth, f" play {depth} {move}")
				print("\t"* depth, self.enemyModel.get_pos())
				self.enemyModel.move(move)
				print("\t"* depth, self.enemyModel.get_pos())
				
				distanceFromPlayer = self.depth_limited_recursive_move(directions, originalMove, preventedPositions, depth-1)
				distancesFromPlayer.append(distanceFromPlayer)
				print("\t"* depth, f"undo {depth} {move}")
				print("\t"* depth, self.enemyModel.get_pos())
				self.enemyModel.undo_move()
				print("\t"* depth, self.enemyModel.get_pos())
		
		minDist = min(distancesFromPlayer)
		print("\t"* depth, f"{distancesFromPlayer} minDist={minDist}")
		return minDist

	def decide_on_movement(self, directions, preventedPositions):
		# transition back to random moves if the player is now out of range
		if not self.player_within_range():
			newState = RandomAIState(self.playerController, self.enemyController, self.enemyModel)
			self.enemyController.update_state(newState)
			return newState.decide_on_movement(directions, preventedPositions)

		# make sure that the same position isn't checked twice when
		# two moves lead to the same location 
		# (like right -> up goes to the same place as up -> right, so only check one of them)
		checkedPositions = {self.enemyModel.get_pos()}

		# append moves to this, and take a copy of the first element when a path to the
		# player is found or a new minimum is found.
		moveStack = []

		

		# XXX now you need 2 things:
		# - the transposition table
		# - move all the code into a single function (don't 
		#   repeat yourself outside the depth_limited_recursive_move function)

		# XXX perform lookahead by self.lookahead moves
		# keep track of the minimum distance to the player
		# pick the move that gets the enemy closest
		minDistToPlayer = infinity
		selectedMovements = []
		depth = 5
		for move in directions:
			if self.movement_allowed(move, preventedPositions):
				print("\t"* depth, f" play {depth} {move}")
				print("\t"* depth, self.enemyModel.get_pos())
				self.enemyModel.move(move)
				print("\t"* depth, self.enemyModel.get_pos())

				minDist = self.depth_limited_recursive_move(directions, move, preventedPositions, depth-1)
				if minDist < minDistToPlayer:
					print(f"minDist for move {move} is {minDist}")
					selectedMovements = [move]
					minDistToPlayer = minDist
				elif minDist == minDistToPlayer:
					print(f"could also do {move}")
					selectedMovements.append(move)

				print("\t"* depth, f"undo {depth} {move}")
				print("\t"* depth, self.enemyModel.get_pos())
				self.enemyModel.undo_move()
				print("\t"* depth, self.enemyModel.get_pos())

		
		selectedMovement = None
		minDistToPlayer = infinity
		for movement in selectedMovements:
			proposedMovementDistance = self.get_speculative_distance_to_player(movement)
			if proposedMovementDistance < minDistToPlayer:
				print(f"chose {selectedMovement} cause it has distance {minDistToPlayer}")
				selectedMovement = movement
				minDistToPlayer = proposedMovementDistance

			

		print(f"minimum distance I can get to player is {minDistToPlayer} with a {selectedMovement}")
		return selectedMovement

# at each level (except base case), call recursive function on all moves and collect results in hash 
# then take minimum of the hash and return it

# when at base case, evaluate distance from player and return it, 

class RandomAIState(AIState):

	def __init__(self, playerController, enemyController, enemyModel):
		super().__init__(playerController, enemyController, enemyModel)
		self.previousMove = None # XXX use this to make the random player walk in straight lines until they can't

	def decide_on_movement(self, directions, preventedPositions):
		# transition to attack state if in range of player and let that state decide
		if self.player_within_range():
			newState = NPlyLookaheadAIState(self.playerController, self.enemyController, self.enemyModel)
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

		beginningAIState = RandomAIState(self.playerController, self, self._characterModel) # XXX pass this in # XXX this needs a major refactor, the enemy controller should not be what is used here, instead it should be the characterModel 
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