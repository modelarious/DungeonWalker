from views.ViewBaseClass import ViewBaseClass
import pygame
from settings import charSet

# draws the grid to the screen using the board model
class MapView(ViewBaseClass):
	def __init__(self):
		pass
		
	def updateView(self, game_screen, mapModel):
		for row in mapModel._board:
			print("".join(row).replace(charSet["pathTemp"], charSet["passable"]).replace(charSet["anchor"],
																						 charSet["passable"]))
		print()
