from abc import ABC, abstractmethod

# defines an interface that all controllers must provide
class ControllerBaseClass(ABC):
	@abstractmethod
	def updateView(self, game_screen):
		pass
