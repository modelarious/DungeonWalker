from orchestrators.EnemyOrchestrator import EnemyOrchestrator

# XXX entirely boilerplate.. is this needed?
class EnemyOrchestratorFactory:
    def __init__(self, enemyControllerFactory, mapController, playerController):
        self.enemyControllerFactory = enemyControllerFactory
        self.mapController = mapController
        self.playerController = playerController

    def getOrchestrator(self):
        return EnemyOrchestrator(self.enemyControllerFactory, self.mapController, self.playerController)