from abc import ABC, abstractmethod

# defines an interface that all views must provide
class ViewBaseClass(ABC):
	@abstractmethod
	def updateView(self, game_screen, model):
		pass
