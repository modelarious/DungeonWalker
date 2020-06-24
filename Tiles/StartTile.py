from Tiles.TileInterface import TileInterface
import pygame
class StartTile(TileInterface):
    def get_char(self):
        return "S"
    
    # responsibility of this class to draw itself in the boundaries given
    def draw_pygame_representation(self, game_screen, minX, maxX, minY, maxY):

        super().draw_pygame_representation(game_screen, minX, maxX, minY, maxY)

        def avg(p1, p2):
            return (p1 + p2) // 2
        
        WHITE = (255, 255, 255)
        #draw an x in the space alotted
        pygame.draw.line(game_screen, WHITE, (minX, avg(minY, maxY)), (maxX, avg(minY, maxY)))
        pygame.draw.line(game_screen, WHITE, (avg(minX, maxX), minY), (avg(minX, maxX), maxY))