from Tiles.TileInterface import TileInterface
import pygame
class GoalTile(TileInterface):
    def get_char(self):
        return "G"
    
    # responsibility of this class to draw itself in the boundaries given
    def draw_pygame_representation(self, game_screen, minX, maxX, minY, maxY):
        BLACK = (255, 255, 255)
        #draw an x in the space alotted
        pygame.draw.line(game_screen, BLACK, (minX, minY), (maxX, maxY))
        pygame.draw.line(game_screen, BLACK, (maxX, minY), (minX, maxY))