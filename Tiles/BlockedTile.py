from Tiles.TileInterface import TileInterface
import pygame
from helpers.Colors import WHITE

class BlockedTile(TileInterface):
    def get_char(self):
        return "`"
    
    # responsibility of this class to draw itself in the boundaries given
    def draw_pygame_representation(self, game_screen, minX, maxX, minY, maxY):
        r = pygame.Rect(minX, minY, maxX-minX, maxY-minY)
        pygame.draw.rect(game_screen, WHITE, r)
