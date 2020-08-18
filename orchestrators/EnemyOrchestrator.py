from helpers.ManhattenDistance import manhatten_distance
class EnemyOrchestrator:
    def __init__(self, enemyControllerFactory, mapController, playerController):
        self.enemyControllerFactory = enemyControllerFactory
        self.playerController = playerController
        self.mapController = mapController

        self.enemyControllerArray = None
        self.generate_new_enemies()
 
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
        # XXX should probably be excluding the current position of the current enemy in each of these - this is because we currently prevent an enemy from staying on the space they are currently on
        preventedPositions = []
        for enemy in self.enemyControllerArray:
            preventedPositions.append(enemy.get_pos())

        # sort enemies by manhatten_distance to player to prevent them from blocking each other when moving
        enemiesSortedByDistanceToPlayer = sorted(
            self.enemyControllerArray, 
            key=lambda e : manhatten_distance(*e.get_pos(), *self.playerController.get_pos())
        )

        # update the enemy positions. Make sure the current enemy's position isn't included in the blacklist.
        # When the position updates, the new enemy position becomes blacklisted
        for enemyController in enemiesSortedByDistanceToPlayer:
            previousPosition = enemyController.get_pos()
            preventedPositions.remove(previousPosition)

            enemyController.update_position(preventedPositions)

            preventedPositions.append(enemyController.get_pos())
    
    def remove_enemy_from_player_position(self):
        playerPos = self.playerController.get_pos()
        
        # XXX could replace this with some functional programming using filter()
        # ..... or the pythonic approach of using list comprehension
        newEnemyArray = []
        for enemy in self.enemyControllerArray:
            enemyPos = enemy.get_pos()
            if enemyPos != playerPos:
                newEnemyArray.append(enemy)
                
        self.enemyControllerArray = newEnemyArray

    def generate_new_enemies(self):
        enemyControllerArray = []
        for spawnCoords in self.mapController.get_enemy_spawn_points():
            enemyControllerArray.append(self.enemyControllerFactory.get_enemy(spawnCoords))
        self.enemyControllerArray = enemyControllerArray