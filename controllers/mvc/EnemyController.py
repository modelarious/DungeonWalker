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

class BFSQueueEntry:
	def __init__(self, initialMovementFromStartTile, positionBeforeApplyingMove, moveToApply, depth=0, debugStack=[]):
		self.initialMove = initialMovementFromStartTile
		self.currentPosition = positionBeforeApplyingMove
		self.currentMove = moveToApply
		self.depth = depth
		self.debugStack = debugStack

	def get_current_position(self):
		return self.currentPosition

	def get_current_move(self):
		return self.currentMove
	
	def get_initial_move(self):
		return self.initialMove
	
	def get_depth(self):
		return self.depth
	
	def get_debug_stack(self):
		return self.debugStack

# NOTE: this is not something like minimax, it's not even A*,
# it's flood-filling to find the directions that the enemy can walk that 
# can put them closest to the player in N moves -> also using Dynamic Programming
# to ensure when a state is first seen, it's at it's MIN distance from the starting node
class NPlyLookaheadAIState(AIState):

	def _create_initial_search_queue(self, directions, preventedPositions):
		q = Queue()

		for initialMove in directions:
			if self.movement_allowed(initialMove, preventedPositions):
				# initialMove will stay constant throughout execution of this algo (basically saying
				# that the current position was reached when the very first movement was initialMove)

				# currentPosition will be the position before you apply the current move
				currentPosition = self.enemyModel.get_pos()

				# currentMove is the move that you want to apply next in the BFS search
				# as this is the first move, the currentMove and initialMove are the same
				currentMove = initialMove 
				q.put(BFSQueueEntry(initialMove, currentPosition, currentMove, 0, [initialMove])) # XXX remove 0 and debug stack
		
		return q

	# XXX should use a MockEnemy object to apply all the transformations... or at least a copy
	# of the enemyModel, cause otherwise you'll be adding to the move queue and not undoing
	
	# The first time a position is reached on the board will automatically be the shortest distance
	# as we're searching breadth first.  Because of this, we can prune search from spaces we've seen 
	# before and we can return immediately when we find the player (two things we couldn't do when using
	# depth limited dfs)
	def breadth_first_search_depth_limited(self, directions, preventedPositions, depthLimit):


		# XXX I figured out the problem -> the enemy will take the most efficient movement that it can
		# XXX even if that means that it will take a step in a bad direction for one turn because the
		# XXX way forward is currently blocked. To prevent this - scrap the preventedPositions system
		# XXX and make a system where all the enemies propose a position they would like to go, then 
		# XXX each is resolved in order - and if two enemies provide the same position, then first come
		# XXX first serve. Basically pretend that the other enemies don't exist when you choose how
		# XXX to move.......... but sometimes the best move is one that has to do with what to do if
		# XXX another enemy is directly beside you - Could it be possible that you need a system that
		# XXX tries all possible ways of resolving the movements and chooses the one that provides the
		# XXX least overall preventions?

		# XXX ACTUALLY YOU NEED TO ORDER THE MOVES BY HEIGHT AND BREAK TIES BY WIDTH..... NO THAT WON'T
		# XXX WORK IN THE CASE THAT PURSUIT IS DOWNWARDS - fuck!!!

		# XXX XXX XXX XXX XXX I GOT IT!!!! Decide move order based on distance to player!!!!!!!!!!!!
		preventedPositions = [ p for p in preventedPositions if p != self.enemyModel.get_pos()]

		

		# XXX ??? does preventedPositions contain the position of the enemy we're currently inspecting???
		# XXX if it does, then the enemy will NEVER use NullMove() because their current position is
		# prevented

		# XXX does preventedPositions update after an enemy moves?

		# XXX could change this to a priority queue and it would be like A*
		searchQueue = self._create_initial_search_queue(directions, preventedPositions) 

		bestMove = NullMove()
		minDistToPlayer = infinity
		seen = set()
		XXXFinalDebugStack = []

		originalPos = self.enemyModel.get_pos()# XXX this is adding to the undo stack on the enemy - 

		# XXX grab the initial position of the enemy and reset it after doing the search / or take a copy of the enemy model


		while not searchQueue.empty():
			
			bFSQueueEntry = searchQueue.get()
			# breakpoint()

			# warp the enemy to the correct position to perform the next move
			currentPosition = bFSQueueEntry.get_current_position()
			self.enemyModel.set_pos(*currentPosition)

			# perform the requested move
			currentMove = bFSQueueEntry.get_current_move()
			self.enemyModel.move(currentMove)

			# if this position has been reached before, skip it
			posAfterMove = self.enemyModel.get_pos()
			if posAfterMove in seen:
				continue

			# now we've seen this position for the first time, track that fact so we don't duplicate work
			# later on in the algo
			seen.add(posAfterMove)

			# if this is the closest we've been to the player, track the initial move that lead us here
			updatedDistanceToPlayer = self.get_distance_to_player()
			initialMove = bFSQueueEntry.get_initial_move()
			if updatedDistanceToPlayer < minDistToPlayer:
				print("got to a lower disttance")
				# breakpoint()
				bestMove = initialMove
				minDistToPlayer = updatedDistanceToPlayer
				XXXFinalDebugStack = bFSQueueEntry.get_debug_stack()

				# end evaluation early if we find the player 
				if updatedDistanceToPlayer == 0:
					print("FOUND YOU PLAYER!!!")
					break # XXX does this actually break out of the top level for loop? XXX are you fucking dumb??
			
			# add all valid next moves to the bfs queue if we haven't reached the depth limit yet
			currDepth = bFSQueueEntry.get_depth()

			XXXDebugStack = bFSQueueEntry.get_debug_stack()
			if currDepth < depthLimit:
				for nextMove in directions:
					# breakpoint()
					if self.movement_allowed(nextMove, preventedPositions):
						nextPos = self.enemyModel.get_speculative_position(nextMove)
						if nextPos not in seen:
							nextLayerDebugStack = XXXDebugStack + [nextMove]
							newBFSQueueEntry = BFSQueueEntry(initialMove, posAfterMove, nextMove, currDepth+1, nextLayerDebugStack)
							searchQueue.put(newBFSQueueEntry)
		self.enemyModel.set_pos(*originalPos)
		print(XXXFinalDebugStack)
		print("playing", bestMove)
		# breakpoint()
		return bestMove

	def decide_on_movement(self, directions, preventedPositions):
		# transition back to random moves if the player is now out of range
		# XXX do the transition after... is there some way to enforce this?
		if not self.player_within_range():
			newState = RandomAIState(self.playerController, self.enemyController, self.enemyModel)
			self.enemyController.update_state(newState)
			return newState.decide_on_movement(directions, preventedPositions)

		
		return self.breadth_first_search_depth_limited(directions, preventedPositions, 20)

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