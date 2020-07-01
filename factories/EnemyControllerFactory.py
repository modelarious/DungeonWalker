from controllers.mvc.PlayerController import EnemyController
from views.CharacterView import CharacterView
from models.CharacterModel import CharacterModel

class EnemyControllerFactory:
    def __init__(self, mapController, playerController):
        self.mapController = mapController
        self.playerController = playerController
    
    def get_enemy(self):
        from random import randint
        characterModel = CharacterModel(randint(0, 10),randint(0, 10))
        RED = (255, 0, 0)
        characterView = CharacterView(grid_size=32, color=RED)
        return EnemyController(characterView, characterModel, self.mapController, self.playerController)