from views.ViewBaseClass import ViewBaseClass
import pygame
from oldsettings import charSet

# draws the character to the screen
class CharacterView(ViewBaseClass):
	def __init__(self, grid_size, color, camera=None):
		self.grid_size = grid_size
		self.color = color
		self.camera = camera
		
	def updateView(self, game_screen, character_model):
		if self.camera:
			x, y = self.camera.get_player_draw_position()
		else:
			x, y = character_model.get_pos()
		x, y = x * self.grid_size, y * self.grid_size

		#draw a square to represent the character
		r = pygame.Rect(x, y, self.grid_size, self.grid_size)
		pygame.draw.rect(game_screen, self.color, r)