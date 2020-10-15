from views.ViewBaseClass import ViewBaseClass
import pygame
from helpers.Colors import BLACK

# draws the grid to the screen using the board model
class GridView(ViewBaseClass):	
	def _drawLines(self, game_screen, lineGenerator):
		for start_point, end_point in lineGenerator():
			pygame.draw.line(game_screen, BLACK, start_point, end_point)
		
	def updateView(self, game_screen, gridModel):
		# self._drawLines(game_screen, gridModel.horizontal_lines)
		# self._drawLines(game_screen, gridModel.vertical_lines)
		pass
