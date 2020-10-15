from controllers.mvc.EnemyController import EnemyController
from views.CharacterView import CharacterView
from models.CharacterModel import CharacterModel
from random import randint
from helpers.Colors import RED

class EnemyControllerFactory:
    def __init__(self, mapModel, playerModel, grid_size):
        self.mapModel = mapModel
        self.playerModel = playerModel
        self.grid_size = grid_size
    
    def get_enemy(self, spawnCoords):
        enemyModel = CharacterModel(*spawnCoords)
        enemyView = CharacterView(grid_size=self.grid_size, color=RED)
        return EnemyController(enemyView, enemyModel, self.mapModel, self.playerModel)