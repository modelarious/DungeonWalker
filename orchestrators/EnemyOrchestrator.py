class EnemyOrchestrator:
    def __init__(self, enemyControllerArray, playerController):
        self.enemyControllerArray = enemyControllerArray
        self.playerController = playerController

    # XXX oh dear........ you really need to return the model and the controller from factories
    # XXX so that you don't have these really dumb calls that ask the controller to ask the model something.
    # XXX you should really be passing the model into this class and not the controller
    def enemy_hit_player(self):
        playerPos = self.playerController.get_pos()
        for enemy in self.enemyControllerArray:
            enemyPos = enemy.get_pos()
            if enemyPos == playerPos:
                return True
                
        return False

    def updateView(self, gameScreen):
        for enemyController in self.enemyControllerArray:
            enemyController.updateView(gameScreen)
        
    def react_to_player(self):
        for enemyController in self.enemyControllerArray:
            enemyController.update_position()