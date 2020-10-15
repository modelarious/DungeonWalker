from factories.GridControllerFactory import GridControllerFactory
from factories.MapControllerMapModelFactory import MapControllerMapModelFactory
from factories.PlayerControllerPlayerModelFactory import PlayerControllerPlayerModelFactory
from factories.EnemyOrchestratorFactory import EnemyOrchestratorFactory
from factories.EnemyControllerFactory import EnemyControllerFactory
from engines.GameEngine import GameEngine
from helpers.Camera import Camera

# XXX make sure that no controllers are being passed into other controllers

grid_size = 48
max_x_dim = 24
max_y_dim = 15

camera = Camera(max_x_dim, max_y_dim)
max_x = grid_size * max_x_dim #1024 32*32
max_y = grid_size * max_y_dim #768 32*24

# max_x = 1248
# max_y = 768

gridController = GridControllerFactory(
    max_x=max_x, max_y=max_y, grid_size=grid_size
).getController()

mapController, mapModel = MapControllerMapModelFactory(
    max_x_tiles=max_x//grid_size*4,
    max_y_tiles=max_y//grid_size*4,
    grid_size=grid_size,
    camera=camera
).getController()

playerController, playerModel = PlayerControllerPlayerModelFactory(
    grid_size=grid_size,
    mapModel=mapModel,
    camera=camera
).getController()

enemyControllerFactory = EnemyControllerFactory(mapModel, playerModel, grid_size, camera)

enemyOrchestrator = EnemyOrchestratorFactory(
    enemyControllerFactory=enemyControllerFactory,
    mapController=mapController,
    playerModel=playerModel
).getOrchestrator()

# observer pattern used to generate enemy spawns when the map is regenerated
mapController.register_enemy_orchestrator(enemyOrchestrator)

# state that we want to watch the player (though we could attach this to an enemy if desired)
camera.watch_character(playerModel)
# we want to watch the current board (and not the minimap, for example)
camera.watch_map(mapModel)

gameEngine = GameEngine(gridController, mapController, playerController, enemyOrchestrator)

gameEngine.main_loop()
