from views.ViewBaseClass import ViewBaseClass
import pygame
from oldsettings import charSet


# draws the grid to the screen using the board model
class MapView(ViewBaseClass):
	def __init__(self):
		pass
		
	def updateView(self, game_screen, mapModel):
		grid_size = 32
		y = 0
		for row in mapModel._board:

			#XXX this is what needs to be updated, it needs to move maxX, minX, maxY, and minY as it moves through the rows and columns
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
