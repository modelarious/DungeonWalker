from controllers.mvc.ControllerBaseClass import ControllerBaseClass

# type hints
from controllers.mvc.MapController import MapController
from models.PlayerCharacterModel import PlayerCharacterModel
from views.PlayerCharacterView import PlayerCharacterView

# XXX will likely move this to another class
import pygame
from helpers.Direction import *


class PlayerController(ControllerBaseClass):
	def __init__(self, 
			playerCharacterView: PlayerCharacterView, 
			playerModel: PlayerCharacterModel, 
			mapController: MapController ):

		self._playerCharacterView = playerCharacterView
		self._player = playerModel
		self._mapController = mapController
	
	def updateView(self, game_screen):
		self._playerCharacterView.updateView(game_screen, self._player)
	
	def handleInputEvent(self, event):
		
		if event.type == pygame.KEYDOWN:
			direction = None
		
			# XXX should be a map
			if event.key == pygame.K_LEFT:
				direction = Left()
			elif event.key == pygame.K_RIGHT:
				direction = Right()
			elif event.key == pygame.K_UP:
				direction = Up()
			elif event.key == pygame.K_DOWN:
				direction = Down()
			else:
				return False

			self._player.move(direction)

			return True
		
		return False



	# def applyMove(self):
	# 	board = self.mapController.get_map()
	# 	self.player.get_pos()
