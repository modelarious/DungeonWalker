import pygame, sys
from pygame.locals import *


# all other views are going to accept the pygame instance.
# this controller controls all the other controllers (which have their own little MVC loop).
# when a controller says it has updated it's model, it is queued up to have .updateView(game_screen, model_response) called on it.
# the queue needs to be ordered properly so we draw things in the right order.
# 
# this controller will pass the pygame instance and model response into them

# XXX need a controller orchestrator that will know which order to draw things in
class GameController(object):
	
	def __init__(self, gridController):
		pygame.init()
		self.gridController = gridController
		self.game_screen = pygame.display.set_mode(gridController.getGameDimensions())
		
	
	def main_loop(self):
		
		# run the game loop
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
					
				# draw the grid
				self.gridController.updateView(self.game_screen)
		
				# draw the window onto the screen
				pygame.display.update()
		