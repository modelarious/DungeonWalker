from Tiles.TileInterface import TileInterface
import pygame

class BlockedTile(TileInterface):
    def get_char(self):
        return "`"
    
    # responsibility of this class to draw itself in the boundaries given
    def draw_pygame_representation(self, game_screen, minX, maxX, minY, maxY):
        WHITE = (255, 255, 255)
        r = pygame.Rect(minX, minY, maxX-minX, maxY-minY)
        pygame.draw.rect(game_screen, WHITE, r)
