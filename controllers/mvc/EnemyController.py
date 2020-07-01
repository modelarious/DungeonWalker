from controllers.mvc.CharacterController import CharacterController

from helpers.Direction import Left, Right, Up, Down

from random import choice

# type hints
from controllers.mvc.MapController import MapController
from models.CharacterModel import CharacterModel
from views.CharacterView import CharacterView
from controllers.mvc.PlayerController import PlayerController


# XXX might be better not to give the enemy controller the player controller but instead an object that
# wraps the player model and lets the enemy make queries about the player 
class EnemyController(CharacterController):
	def __init__(self, 
			characterView: CharacterView,
			characterModel: CharacterModel,
			mapController: MapController,
			playerController: PlayerController ):
		super().__init__(characterView, characterModel, mapController)
		self.playerController = playerController

	def update_position(self):
		direction = choice([Right(), Left(), Up(), Down()])
		self._characterModel.move(direction)