class EnemyOrchestrator:
    def __init__(self, enemyControllerArray):
        self.enemyControllerArray = enemyControllerArray

    def updateView(self, gameScreen):
        for enemyController in self.enemyControllerArray:
            enemyController.updateView(gameScreen)
        
    def react_to_player(self):
        for enemyController in self.enemyControllerArray:
            enemyController.update_position()