from Tiles.TileInterface import TileInterface
import pygame
class PassableTile(TileInterface):
    def get_char(self):
        return "*"
    
    # responsibility of this class to draw itself in the boundaries given
    def draw_pygame_representation(self, game_screen, minX, maxX, minY, maxY):
        BLACK = (0, 0, 0)
        r = pygame.Rect(minX, minY, maxX-minX, maxY-minY)
        pygame.draw.rect(game_screen, BLACK, r)