from controllers.mvc.EnemyController import EnemyController
from views.CharacterView import CharacterView
from models.CharacterModel import CharacterModel
from random import randint

class EnemyControllerFactory:
    def __init__(self, mapModel, playerModel, grid_size):
        self.mapModel = mapModel
        self.playerModel = playerModel
        self.grid_size = grid_size
    
    def get_enemy(self, spawnCoords):
        enemyModel = CharacterModel(*spawnCoords)
        RED = (255, 0, 0) # XXX define all colors in one spot instead of all over the place
        enemyView = CharacterView(grid_size=self.grid_size, color=RED)
        return EnemyController(enemyView, enemyModel, self.mapModel, self.playerModel)