import pygame, sys
from pygame.locals import *

# Handle events to update game state
# this controller controls all the other controllers (which each have their own little MVC loop).
# I didn't use the observer pattern because the pieces of the screen need to be drawn in a particular order
class GameController(object):
	def __init__(self, gridController, mapController, playerController):
		pygame.init()
		self.gridController = gridController
		self.mapController = mapController
		self.playerController = playerController
		self.game_screen = pygame.display.set_mode(gridController.getGameDimensions())

	
	def draw_game(self):

		# draw the camera's view of the map to the screen
		self.mapController.updateView(self.game_screen)

		# draw the grid
		self.gridController.updateView(self.game_screen)

		# draw the player to the screen
		self.playerController.updateView(self.game_screen)

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
					
					if self.playerController.player_has_won():
						print("player is a winner!")
						self.mapController.generate_new_map()
						self.playerController.place_player_at_start()
					
					self.draw_game()


			