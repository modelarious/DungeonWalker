from helpers.Direction import Left
from controllers.mvc.PlayerController import EnemyController
from views.CharacterView import CharacterView
from models.CharacterModel import CharacterModel


class EnemyOrchestratorFactory:
    def __init__(self, mapController, playerController):
        self.mapController = mapController
        self.playerController = playerController

    def getOrchestrator(self):
        # enemyControllerArray = EnemyControllerArrayFactory()

        # enemy factory
        enemyControllerArray = []

        from random import randint

        for _ in range(7):
            cm = CharacterModel(randint(0, 10),randint(0, 10))
            BLUE = (255, 0, 0)
            cv = CharacterView(grid_size=32, color=BLUE)
            cc = EnemyController(cv, cm, self.mapController, self.playerController)

            enemyControllerArray.append(cc)

        return EnemyOrchestrator(self.mapController, self.playerController, enemyControllerArray)

class EnemyOrchestrator:
    def __init__(self, mapController, playerController, enemyControllerArray):
        self.mapController = mapController
        # self.playerController = playerController
        self.enemyControllerArray = enemyControllerArray

    def updateView(self, gameScreen):
        for enemyController in self.enemyControllerArray:
            enemyController.updateView(gameScreen)
        
    def react_to_player(self):
        for enemyController in self.enemyControllerArray:
            enemyController.update_position()