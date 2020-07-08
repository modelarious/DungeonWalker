from views.ViewBaseClass import ViewBaseClass
import pygame
from oldsettings import charSet

# draws the character to the screen
class CharacterView(ViewBaseClass):
	def __init__(self, grid_size, color):
		self.grid_size = grid_size
		self.color = color
		
	def updateView(self, game_screen, character_model):
		x, y = character_model.get_pos()
		x, y = x * self.grid_size, y * self.grid_size

		#draw a square to represent the character
		r = pygame.Rect(x, y, self.grid_size, self.grid_size)
		pygame.draw.rect(game_screen, self.color, r)