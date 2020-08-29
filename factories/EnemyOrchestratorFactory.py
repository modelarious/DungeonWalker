from orchestrators.EnemyOrchestrator import EnemyOrchestrator

class EnemyOrchestratorFactory:
    def __init__(self, enemyControllerFactory, mapController, playerModel):
        self.enemyControllerFactory = enemyControllerFactory
        self.mapController = mapController
        self.playerModel = playerModel

    def getOrchestrator(self):
        return EnemyOrchestrator(self.enemyControllerFactory, self.mapController, self.playerModel)