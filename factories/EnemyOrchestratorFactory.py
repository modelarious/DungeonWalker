from orchestrators.EnemyOrchestrator import EnemyOrchestrator

class EnemyOrchestratorFactory:
    def __init__(self, enemyControllerFactory, enemySpawnPoints):
        self.enemyControllerFactory = enemyControllerFactory
        self.enemySpawnPoints = enemySpawnPoints

    def getOrchestrator(self):
        enemyControllerArray = []
        for spawnCoords in self.enemySpawnPoints:
            enemyControllerArray.append(self.enemyControllerFactory.get_enemy(spawnCoords))
        return EnemyOrchestrator(enemyControllerArray)