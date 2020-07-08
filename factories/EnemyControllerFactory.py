from controllers.mvc.EnemyController import EnemyController
from views.CharacterView import CharacterView
from models.CharacterModel import CharacterModel
from random import randint

class EnemyControllerFactory:
    def __init__(self, mapController, playerController):
        self.mapController = mapController
        self.playerController = playerController
    
    def get_enemy(self, spawnCoords):
        characterModel = CharacterModel(*spawnCoords)
        RED = (255, 0, 0)
        characterView = CharacterView(grid_size=32, color=RED)
        return EnemyController(characterView, characterModel, self.mapController, self.playerController)