from Tiles.TileInterface import TileInterface
class GoalTile(TileInterface):
    def get_char(self):
        return "G"
    
    # responsibility of this class to draw itself in the boundaries given
    def draw_pygame_representation(self, game_screen, minX, maxX, minY, maxY):
        pass