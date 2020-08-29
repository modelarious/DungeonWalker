from controllers.mvc.CharacterController import CharacterController

from helpers.Direction import Left, Right, Up, Down, NullMove

from random import shuffle
from queue import Queue
from helpers.ManhattenDistance import manhatten_distance

# type hints
from controllers.mvc.MapController import MapController
from models.CharacterModel import CharacterModel
from views.CharacterView import CharacterView
from controllers.mvc.PlayerController import PlayerController

infinity = 999999999

class AIState:
	def __init__(self, playerModel, enemyModel, mapModel, enemyController):
		self.playerModel = playerModel
		self.enemyModel = enemyModel
		self.mapModel = mapModel
		self.enemyController = enemyController # to update the AI state
		self.lookahead = 7

	def decide_on_movement(self, directions, preventedPositions):
		pass

	def player_within_range(self):
		# consider transitioning to attack state if in range of player
		N = self.lookahead
		if self.get_distance_to_player(self.enemyModel) <= N:
			return True
		return False
	
	def get_distance_to_player(self, iEnemyModel):
		playerPosition = self.playerModel.get_pos()
		return manhatten_distance(*playerPosition, *iEnemyModel.get_pos())
	
	def get_speculative_distance_to_player(self, iEnemyModel, move):
		playerPosition = self.playerModel.get_pos()
		return manhatten_distance(*playerPosition, *iEnemyModel.get_speculative_position(move))

	# check if this is a legal move
	def movement_allowed(self, move, preventedPositions, iEnemyModel):
		return iEnemyModel.movement_valid(move, self.mapModel) and not iEnemyModel.movement_prevented(move, preventedPositions)
	
	# this is a state in which the enemy has landed on the player
	# XXX either use it, or get rid of it
	def is_winning_state(self, position):
		return self.playerModel.get_pos() == position

class BFSQueueEntry:
	def __init__(self, initialMovementFromStartTile, positionBeforeApplyingMove, moveToApply, depth=0):
		self.initialMove = initialMovementFromStartTile
		self.currentPosition = positionBeforeApplyingMove
		self.currentMove = moveToApply
		self.depth = depth

	def get_current_position(self):
		return self.currentPosition

	def get_current_move(self):
		return self.currentMove
	
	def get_initial_move(self):
		return self.initialMove
	
	def get_depth(self):
		return self.depth

# NOTE: this is not something like minimax, it's not even A*,
# it's flood-filling to find the directions that the enemy can walk that 
# can put them closest to the player in N moves -> also using Dynamic Programming
# to ensure when a state is first seen, it's at it's MIN distance from the starting node
class NPlyLookaheadAIState(AIState):

	def _create_initial_search_queue(self, directions, preventedPositions):
		q = Queue()

		for initialMove in directions:
			if self.movement_allowed(initialMove, preventedPositions, self.enemyModel):
				# initialMove will stay constant throughout execution of this algo (basically saying
				# that the current position was reached when the very first movement was initialMove).
				# If we find the player then we want to attribute it to the correct initial move

				# currentPosition will be the position before you apply the current move
				currentPosition = self.enemyModel.get_pos()

				# currentMove is the move that you want to apply next in the BFS search.
				# As this is the first move, the currentMove and initialMove are the same
				currentMove = initialMove 
				q.put(BFSQueueEntry(initialMove, currentPosition, currentMove))
		
		return q

	# Using a MockEnemy object to apply all the transformations, cause otherwise it'll be 
	# adding to the move queue for the enemy model and not undoing
	
	# The first time a position is reached on the board will automatically be the shortest distance
	# as we're searching breadth first.  Because of this, we can prune search from spaces we've seen 
	# before and we can return immediately when we find the player (two things we couldn't do when using
	# depth limited dfs)
	def breadth_first_search_depth_limited(self, directions, preventedPositions, depthLimit):

		# XXX could change this to a priority queue based on distance to player and it would be A*
		searchQueue = self._create_initial_search_queue(directions, preventedPositions) 

		bestMove = NullMove()
		minDistToPlayer = infinity
		seen = set()

		enemyClone = self.enemyModel.get_copy()
		while not searchQueue.empty():
			bFSQueueEntry = searchQueue.get()

			# warp the enemy to the correct position to perform the next move
			currentPosition = bFSQueueEntry.get_current_position()
			enemyClone.set_pos(*currentPosition)

			# perform the requested move
			currentMove = bFSQueueEntry.get_current_move()
			enemyClone.move(currentMove)

			# if this position has been reached before, skip it
			posAfterMove = enemyClone.get_pos()
			if posAfterMove in seen:
				continue

			# now we've seen this position for the first time, track that fact so we don't duplicate work
			# later on in the algo
			seen.add(posAfterMove)

			# if this is the closest we've been to the player, track the initial move that lead us here
			updatedDistanceToPlayer = self.get_distance_to_player(enemyClone)
			initialMove = bFSQueueEntry.get_initial_move()
			if updatedDistanceToPlayer < minDistToPlayer:
				bestMove = initialMove
				minDistToPlayer = updatedDistanceToPlayer

				# end evaluation early if we find the player 
				if updatedDistanceToPlayer == 0:
					break
			
			# add all valid next moves to the bfs queue if we haven't reached the depth limit yet
			currDepth = bFSQueueEntry.get_depth()
			if currDepth < depthLimit:
				for nextMove in directions:
					if self.movement_allowed(nextMove, preventedPositions, enemyClone):
						nextPos = enemyClone.get_speculative_position(nextMove)
						if nextPos not in seen:
							newBFSQueueEntry = BFSQueueEntry(initialMove, posAfterMove, nextMove, currDepth+1)
							searchQueue.put(newBFSQueueEntry)
		return bestMove

	def decide_on_movement(self, directions, preventedPositions):
		# transition back to random moves if the player is now out of range
		# XXX do the transition after... is there some way to enforce this?
		if not self.player_within_range():
			newState = RandomAIState(self.playerModel, self.enemyModel, self.mapModel, self.enemyController)
			self.enemyController.update_state(newState)
			return newState.decide_on_movement(directions, preventedPositions)

		
		return self.breadth_first_search_depth_limited(directions, preventedPositions, 20)

# at each level (except base case), call recursive function on all moves and collect results in hash 
# then take minimum of the hash and return it

# when at base case, evaluate distance from player and return it, 

class RandomAIState(AIState):

	def __init__(self, playerModel, enemyModel, mapModel, enemyController):
		super().__init__(playerModel, enemyModel, mapModel, enemyController)
		self.previousMove = None # XXX use this to make the random player walk in straight lines until they can't

	def decide_on_movement(self, directions, preventedPositions):
		# transition to attack state if in range of player and let that state decide
		if self.player_within_range():
			newState = NPlyLookaheadAIState(self.playerModel, self.enemyModel, self.mapModel, self.enemyController)
			self.enemyController.update_state(newState)
			return newState.decide_on_movement(directions, preventedPositions)

		# since the enemy is far away from the player, just move randomly
		for move in directions:
			if self.movement_allowed(move, preventedPositions, self.enemyModel):
				return move

		# didn't find a move that worked
		return NullMove()



# XXX type hints
from models.CharacterModel import CharacterModel
from models.MapModel import MapModel

class EnemyController(CharacterController):
	def __init__(self, 
			characterView: CharacterView,
			characterModel: CharacterModel, # enemy model
			mapModel: MapModel,
			playerModel: CharacterModel ):

		super().__init__(characterView, characterModel, mapModel)
		self._playerModel = playerModel

		#XXX should ai state should be a property of the characterModel? maybe I need an enemyModel
		beginningAIState = RandomAIState(self._playerModel, self._characterModel, self._mapModel, self)
		self._AIState = beginningAIState

	def update_position(self, preventedPositions):
		directions = [Right(), Left(), Up(), Down(), NullMove()]
		shuffle(directions)
		move = self._AIState.decide_on_movement(directions, preventedPositions)

		if move == None:
			return False
		
		self._characterModel.move(move)
		return True
	
	# called by the AIState object to update what state the AI is in
	def update_state(self, newState):
		self._AIState = newState