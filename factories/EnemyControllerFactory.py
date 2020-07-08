from controllers.mvc.EnemyController import EnemyController
from views.CharacterView import CharacterView
from models.CharacterModel import CharacterModel
from random import randint

class EnemyControllerFactory:
    def __init__(self, mapController, playerController, grid_size):
        self.mapController = mapController
        self.playerController = playerController
        self.grid_size = grid_size
    
    def get_enemy(self, spawnCoords):
        characterModel = CharacterModel(*spawnCoords)
        RED = (255, 0, 0)
        characterView = CharacterView(grid_size=self.grid_size, color=RED)
        return EnemyController(characterView, characterModel, self.mapController, self.playerController)