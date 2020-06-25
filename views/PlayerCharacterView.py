from views.ViewBaseClass import ViewBaseClass
import pygame
from oldsettings import charSet

# draws the player to the screen
class PlayerCharacterView(ViewBaseClass):
	def __init__(self, grid_size):
		self.grid_size = grid_size
		
	def updateView(self, game_screen, character_model):

		x, y = character_model.get_pos()
		x, y = x * self.grid_size, y * self.grid_size
		GREEN = (0, 255, 0)

		#draw a square for the player
		r = pygame.Rect(x, y, self.grid_size, self.grid_size)
		pygame.draw.rect(game_screen, GREEN, r)