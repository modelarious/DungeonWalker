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
        
    
    # XXX this really needs to be tested to make sure it actually prevents movement
    def react_to_player(self):

        # gather current enemy positions and prevent enemies from moving to an overlapping position
        preventedPositions = []
        for enemy in self.enemyControllerArray:
            preventedPositions.append(enemy.get_pos())

        # update the enemy positions. When the position updates, the new enemy position becomes blacklisted
        # and the old position gets removed from the blacklist
        for enemyController in self.enemyControllerArray:
            previousPosition = enemyController.get_pos()
            enemyController.update_position(preventedPositions)

            preventedPositions.remove(previousPosition)
            preventedPositions.append(enemyController.get_pos())
    
    def remove_enemy_from_player_position(self):
        playerPos = self.playerController.get_pos()
        newEnemyArray = []

        # XXX could replace this with some functional programming using filter()
        for enemy in self.enemyControllerArray:
            enemyPos = enemy.get_pos()
            if enemyPos != playerPos:
                newEnemyArray.append(enemy)
                
        self.enemyControllerArray = newEnemyArray

    
