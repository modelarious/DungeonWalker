from views.ViewBaseClass import ViewBaseClass
import pygame

# draws the tile mapped objects to the screen
class TileMappedView(ViewBaseClass):
	def __init__(self, grid_size, tileMapper):
		self._tileMapper = tileMapper
		self.grid_size = grid_size
		
	def updateView(self, game_screen, minX, maxX, minY, maxY):
		xDelta = maxX - minX
		yDelta = maxY - minY

		for point, tile in self._tileMapper.get_tile_mapping():
			x, y = point
			if x < minX or x >= maxX or y < minY or y >= maxY:
				continue

			scaled_x, scaled_y = (x - minX) * 32, (y - minY) * 24
			scaledPoint = (scaled_x, scaled_y)
			game_screen.blit(tile, scaledPoint)
