from abc import ABC, abstractmethod, abstractproperty
import pygame
class TileInterface(ABC):
    @abstractmethod
    def get_char(self):
        return
    
    # responsibility of this class to draw itself in the boundaries given
    def draw_pygame_representation(self, game_screen, minX, maxX, minY, maxY):
        BLACK = (0, 0, 0)
        r = pygame.Rect(minX, minY, maxX-minX, maxY-minY)
        pygame.draw.rect(game_screen, BLACK, r)