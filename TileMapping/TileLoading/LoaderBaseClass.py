class LoaderBaseClass:
	''' shared tools that can be used by any class that loads from a tileset image '''
	def __init__(self, tilesetImage, gameGridSize):
		# useful local constants
		self.gameGridSize = gameGridSize # the grid_size we are using for display
		self.image = tilesetImage
		self.tileSetGridSize = 24 # each of the square tiles on the image are 24 pixels wide
		self.border = 1 # there is a 1 pixel border around each of the individual square tiles in the image. This border is shared (so the right border of one tile is the left border of the adjacent tile)
		self.scaleFactor = self.tileSetGridSize + self.border # so to jump to the next tile, you need to move the tile width (tileSetGridSize) + the size of the shared border (border)

	def _get_n_by_m_tile_matrix(self, leftX, topY, tileCountInRow, tileCountInColumn, resizeFactor):

		# ignores the border on the left and top
		startX = leftX + self.border
		startY = topY + self.border

		tiles, coordinates = [], []

		# example, get 3x3 -> range to startY + 3*scaleFactor because we are grabbing 3 squares starting from startY
		for yDim in range(startY, startY + tileCountInColumn*self.scaleFactor, self.scaleFactor):
			for xDim in range(startX, startX + tileCountInRow*self.scaleFactor, self.scaleFactor):
				tile = self._crop_and_resize_square_image(xDim, yDim, resizeFactor)
				tiles.append(tile)
				coordinates.append((xDim, yDim))

		return tiles, coordinates

	def _crop_and_resize_square_image(self, leftX, topY, resizeFactor):
		# crop image
		rightX = leftX + self.tileSetGridSize
		bottomY = topY + self.tileSetGridSize
		box = (leftX, topY, rightX, bottomY)
		cropped = self.image.crop(box)

		# resize cropped image
		resized = cropped.resize(resizeFactor)
		return resized