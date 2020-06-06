from views.ViewBaseClass import ViewBaseClass
import pygame
from oldsettings import charSet

# draws the grid to the screen using the board model
class MapView(ViewBaseClass):
	def __init__(self):
		pass
		
	def updateView(self, game_screen, mapModel):
		for row in mapModel._board:

			row = list(map(lambda a : a.get_char(), row))
			# XXX this processing should be done in the board generation step
			print("".join(row).replace(charSet["pathTemp"], charSet["passable"]).replace(charSet["anchor"],
																						 charSet["passable"]))
		print()
