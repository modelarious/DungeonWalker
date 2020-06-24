from views.ViewBaseClass import ViewBaseClass
import pygame
from oldsettings import charSet


# draws the grid to the screen using the map model
class MapView(ViewBaseClass):
	def __init__(self, grid_size):
		self._grid_size = grid_size
		pass
		
	def updateView(self, game_screen, mapModel):
		grid_size = self._grid_size
		y = 0
		for row in mapModel.get_board():
			x = 0
			for tile in row:
				tile.draw_pygame_representation(game_screen, x % 1025, (x + grid_size) % 1025, y % 769, (y + grid_size)% 769)
				x += grid_size

			row = list(map(lambda a : a.get_char(), row))
			
			# XXX this processing should be done in the board generation step
			print("".join(row).replace(charSet["pathTemp"], charSet["passable"]).replace(charSet["anchor"],
																						 charSet["passable"]))
			y += grid_size
		print()
