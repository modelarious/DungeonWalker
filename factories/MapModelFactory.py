from models.MapModel import MapModel
from factories.FactoryBaseClass import FactoryBaseClass

class MapModelFactory(FactoryBaseClass):
	def __init__(self, width, height, autoconnect, mapGenerator):
		self.width = width
		self.height = height
		self.autoconnect = autoconnect
		self.mapGenerator = mapGenerator

	def getMapModel(self):
		#XXX this is ripe for refactor. Most methods in mapModel are used once when creating
		# the board, so these steps could likely be captured elsewhere 
		# (perhaps MapGeneratorBaseClass). and it wouldn't need the autoconnect unit
		emptyMap = MapModel(
			self.get_copy(self.width), 
			self.get_copy(self.height), 
			self.get_copy(self.autoconnect)
		)

		return self.mapGenerator(emptyMap).generateMap()

