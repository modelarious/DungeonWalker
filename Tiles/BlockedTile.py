from TileInterface import TileInterface
class BlockedTile(TileInterface):
    def get_char(self):
        return "`"
    
    # responsibility of this class to draw itself in the boundaries given
    def draw_pygame_representation(self, game_board, minX, maxX, minY, maxY):
        pass