class EnemyOrchestratorFactory:
    def __init__(self, mapController, playerController):
        self.mapController = mapController
        self.playerController = playerController

    def getOrchestrator(self):
        # enemyControllerArray = EnemyControllerArrayFactory()
        enemyControllerArray = []
        return EnemyOrchestrator(self.mapController, self.playerController, enemyControllerArray)

class EnemyOrchestrator:
    def __init__(self, mapController, playerController, enemyControllerArray):
        self.mapController = mapController
        self.playerController = playerController
        self.enemyControllerArray = enemyControllerArray

    def updateView(self, game_screen):
        for enemyController in self.enemyControllerArray:
            pass
        
    def react_to_player(self):
        for enemyController in self.enemyControllerArray:
            pass