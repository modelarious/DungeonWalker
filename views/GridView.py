from views.ViewBaseClass import ViewBaseClass
import pygame

# draws the grid to the screen using the board model
class GridView(ViewBaseClass):
	def __init__(self, colors):
		self.colors = colors
	
	def _drawLines(self, game_screen, lineGenerator):
		for start_point, end_point in lineGenerator():
			pygame.draw.line(game_screen, self.colors.BLACK, start_point, end_point)
		
	def updateView(self, game_screen, gridModel):
		# self._drawLines(game_screen, gridModel.horizontal_lines)
		# self._drawLines(game_screen, gridModel.vertical_lines)
		pass
