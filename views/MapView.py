from views.ViewBaseClass import ViewBaseClass
import pygame
from oldsettings import charSet


# draws the grid to the screen using the map model.
# requires a camera
class MapView(ViewBaseClass):
	def __init__(self, grid_size, tileMapperView, camera):
		self._grid_size = grid_size
		self._tileMapperView = tileMapperView
		self._camera = camera
		
	def updateView(self, game_screen, mapModel):
		grid_size = self._grid_size
		cameraBox = self._camera.get_camera_box(mapModel)

		self._tileMapperView.updateView(game_screen, *cameraBox)
		
		y = 0
		for row in mapModel.get_part_of_board(*cameraBox):
			x = 0
			for tile in row:
				tile.draw_pygame_representation(game_screen, x % 1025, (x + grid_size) % 1025, y % 769, (y + grid_size)% 769) #XXX
				x += grid_size
			y += grid_size
			
			# print the board to the terminal
			char_row = list(map(lambda a : a.get_char(), row))
			
			# XXX this processing should be done in the board generation step
			print("".join(char_row)
				.replace(charSet["pathTemp"], charSet["passable"])
				.replace(charSet["anchor"], charSet["passable"])
			)
		print()

		
