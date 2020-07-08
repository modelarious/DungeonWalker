import pygame, sys
from pygame.locals import *

# Handle events to update game state
# this Engine controls all the other controllers (which each have their own little MVC loop).
# I didn't use the observer pattern because the pieces of the screen need to be drawn in a particular order
class GameEngine(object):
	def __init__(self, gridController, mapController, playerController, enemyOrchestrator):
		pygame.init()
		self.gridController = gridController
		self.mapController = mapController
		self.playerController = playerController
		self.enemyOrchestrator = enemyOrchestrator

		# XXX... why...? just pass the game dimensions into the GameController
		# XXX or better yet, just pass in the game screen? There's no other reason it needs to know the dimensions
		self.game_screen = pygame.display.set_mode(gridController.getGameDimensions())

	def draw_game(self):

		# draw the camera's view of the map to the screen
		self.mapController.updateView(self.game_screen)

		# draw the grid
		self.gridController.updateView(self.game_screen)

		# draw the player to the screen
		self.playerController.updateView(self.game_screen)

		# draw enemies on the screen
		self.enemyOrchestrator.updateView(self.game_screen)

		# draw the window onto the screen
		pygame.display.update()

	def main_loop(self):
		self.draw_game()

		# run the game loop
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				
				if self.playerController.handleInputEvent(event):

					if self.enemyOrchestrator.player_hit_enemy():
						self.enemyOrchestrator.remove_enemy_from_player_position()
					
					if self.playerController.player_has_won():
						self.mapController.generate_new_map()
						self.playerController.place_player_at_start()
					
					else:
						self.enemyOrchestrator.react_to_player()
						if self.enemyOrchestrator.enemy_hit_player():
							print("enemy killed you!")
							return False
					
					self.draw_game()


			