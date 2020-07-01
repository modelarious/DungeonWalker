from orchestrators.EnemyOrchestrator import EnemyOrchestrator

class EnemyOrchestratorFactory:
    def __init__(self, enemyControllerFactory, enemyCount):
        self.enemyControllerFactory = enemyControllerFactory
        self.enemyCount = enemyCount

    def getOrchestrator(self):
        enemyControllerArray = []
        for _ in range(self.enemyCount):
            enemyControllerArray.append(self.enemyControllerFactory.get_enemy())
        return EnemyOrchestrator(enemyControllerArray)