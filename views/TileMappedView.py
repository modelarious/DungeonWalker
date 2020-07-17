from views.ViewBaseClass import ViewBaseClass
import pygame

# draws the tile mapped objects to the screen
class TileMappedView(ViewBaseClass):
	def __init__(self, grid_size, tileMapper):
		self._tileMapper = tileMapper
		self.grid_size = grid_size
		
	def updateView(self, game_screen):
		for point, tile in self._tileMapper.get_tile_mapping():
			x, y = point
			scaled_x, scaled_y = x*self.grid_size, y*self.grid_size
			scaledPoint = (scaled_x, scaled_y)
			game_screen.blit(tile, scaledPoint)
