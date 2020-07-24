from TileMapping.TileLoading.LoaderBaseClass import LoaderBaseClass

class StairLoader(LoaderBaseClass):
    def get_stairs(self):
        return self.stairs

    def process_stairs(self):
        # pixel indices into the image where the stairs live
        left = 13
        top = 387
        tile = self._crop_and_resize_square_image(left, top, (self.gameGridSize, self.gameGridSize))
        self.stairs = self._export_for_pygame_rgb(tile)
