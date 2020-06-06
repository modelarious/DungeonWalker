from views.ViewBaseClass import ViewBaseClass
import pygame

# draws the grid to the screen using the board model
class BoardView(ViewBaseClass):
	def __init__(self, colors):
		self.colors = colors
	
	def _drawLines(self, game_screen, lineGenerator):
		for start_point, end_point in lineGenerator():
			pygame.draw.line(game_screen, self.colors.BLACK, start_point, end_point)
		
	def updateView(self, game_screen, boardModel):
		self._drawLines(game_screen, boardModel.horizontal_lines)
		self._drawLines(game_screen, boardModel.vertical_lines)
