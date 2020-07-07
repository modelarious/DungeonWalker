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
    
    def player_hit_enemy(self):
        # the same calculation is used, so essentially the same function. Names are nice for humans.
        return self.enemy_hit_player()


    def updateView(self, gameScreen):
        for enemyController in self.enemyControllerArray:
            enemyController.updateView(gameScreen)
        
    def react_to_player(self):
        for enemyController in self.enemyControllerArray:
            enemyController.update_position()
    
    def remove_enemy_from_player_position(self):
        playerPos = self.playerController.get_pos()
        newEnemyArray = []

        # XXX could replace this with some functional programming using filter()
        for enemy in self.enemyControllerArray:
            enemyPos = enemy.get_pos()
            if enemyPos != playerPos:
                newEnemyArray.append(enemy)
                
        self.enemyControllerArray = newEnemyArray

    
