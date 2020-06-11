from models.MapModel import MapModel, AdditionController, MapGenerator
from factories.FactoryBaseClass import FactoryBaseClass
from helpers.Autoconnect import Autoconnect

class MapModelFactory(FactoryBaseClass):
	def __init__(self, width, height, mapGenerator):
		self.width = width
		self.height = height
		self.mapGenerator = mapGenerator

	def getMapModel(self):
		emptyMap = MapModel(
			self.get_copy(self.width), 
			self.get_copy(self.height)
		)
		additionController = AdditionController(emptyMap)

		# XXX NAMING HERE, THIS needs distinction from RandomMapGenerator and MapGeneratorBaseClass
		# maybe randommapgenerator could be randommapgenerationcontroller or driver
		mg = MapGenerator(
			self.get_copy(self.width), 
			self.get_copy(self.height),
			Autoconnect(),
			additionController
		)

		return self.mapGenerator(
			self.get_copy(self.width), 
			self.get_copy(self.height),
			mg
		).generateMap()

