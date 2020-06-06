from views.ViewBaseClass import ViewBaseClass
import pygame
from oldsettings import charSet


# draws the grid to the screen using the board model
class MapView(ViewBaseClass):
	def __init__(self):
		pass
		
	def updateView(self, game_screen, mapModel):
		for row in mapModel._board:

			#XXX this is what needs to be updated, it needs to move maxX, minX, maxY, and minY as it moves through the rows and columns
			for x in row:
				x.draw_pygame_representation(game_screen, 0, 32, 0, 32)

			row = list(map(lambda a : a.get_char(), row))
			# XXX this processing should be done in the board generation step
			print("".join(row).replace(charSet["pathTemp"], charSet["passable"]).replace(charSet["anchor"],
																						 charSet["passable"]))
		print()
