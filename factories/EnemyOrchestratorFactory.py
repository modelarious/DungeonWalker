from orchestrators.EnemyOrchestrator import EnemyOrchestrator

class EnemyOrchestratorFactory:
    def __init__(self, enemyControllerFactory):
        self.enemyControllerFactory = enemyControllerFactory

    def getOrchestrator(self):
        enemyControllerArray = []
        enemyCount = 10
        for _ in range(enemyCount):
            enemyControllerArray.append(self.enemyControllerFactory.get_enemy())
        return EnemyOrchestrator(enemyControllerArray)