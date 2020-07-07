from orchestrators.EnemyOrchestrator import EnemyOrchestrator

class EnemyOrchestratorFactory:
    def __init__(self, enemyControllerFactory, enemySpawnPoints, playerController):
        self.enemyControllerFactory = enemyControllerFactory
        self.enemySpawnPoints = enemySpawnPoints
        self.playerController = playerController

    def getOrchestrator(self):
        enemyControllerArray = []
        for spawnCoords in self.enemySpawnPoints:
            enemyControllerArray.append(self.enemyControllerFactory.get_enemy(spawnCoords))
        return EnemyOrchestrator(enemyControllerArray, self.playerController)