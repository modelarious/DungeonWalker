from factories.GridControllerFactory import GridControllerFactory
from factories.MapControllerFactory import MapControllerFactory
from factories.PlayerControllerFactory import PlayerControllerFactory
from factories.EnemyOrchestratorFactory import EnemyOrchestratorFactory
from factories.EnemyControllerFactory import EnemyControllerFactory
from engines.GameEngine import GameEngine


# XXX Get rid of this nonsense
class Colors():
	def __init__(self):
		self.BLACK = (255, 255, 255)

grid_size = 12
# max_x_dim = 32
# max_y_dim = 24

# max_x = grid_size * max_x_dim #1024 32*32
# max_y = grid_size * max_y_dim #768 32*24

max_x = 1024
max_y = 768

colors = Colors()
gridController = GridControllerFactory(
	max_x=max_x, max_y=max_y, grid_size=grid_size, colors=colors
).getController()

mapController = MapControllerFactory(
	max_x_tiles=max_x//grid_size,
	max_y_tiles=max_y//grid_size,
	grid_size=grid_size
).getController()

playerController = PlayerControllerFactory(
	grid_size=grid_size,
	mapController=mapController
).getController()

enemyControllerFactory = EnemyControllerFactory(mapController, playerController, grid_size)

enemyOrchestrator = EnemyOrchestratorFactory(
	enemyControllerFactory=enemyControllerFactory,
	mapController=mapController,
	playerController=playerController
).getOrchestrator()

# observer pattern used to generate enemy spawns when the map is regenerated
mapController.register_enemy_orchestrator(enemyOrchestrator)

gameEngine = GameEngine(gridController, mapController, playerController, enemyOrchestrator)

gameEngine.main_loop()
