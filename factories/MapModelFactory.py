from models.MapModel import MapModel, AdditionController, MapGeneratorEngine
from factories.FactoryBaseClass import FactoryBaseClass
from helpers.Autoconnect import Autoconnect

class MapModelFactory(FactoryBaseClass):
	def __init__(self, width, height, mapGenerationController):
		self.width = width
		self.height = height
		self.mapGenerationController = mapGenerationController

	def getMapModel(self):
		emptyMap = MapModel(
			self.get_copy(self.width), 
			self.get_copy(self.height)
		)
		additionController = AdditionController(emptyMap)

		mapGeneratorEngine = MapGeneratorEngine(
			self.get_copy(self.width), 
			self.get_copy(self.height),
			Autoconnect(),
			additionController
		)

		generatedMapModel = self.mapGenerationController(
			self.get_copy(self.width), 
			self.get_copy(self.height),
			mapGeneratorEngine
		).generateMap()

		return generatedMapModel

