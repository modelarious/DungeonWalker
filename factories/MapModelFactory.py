from models.MapModel import MapModel
from controllers.AdditionController import AdditionController
from engines.MapGeneratorEngine import MapGeneratorEngine
from factories.FactoryBaseClass import FactoryBaseClass
from helpers.Autoconnect import Autoconnect

class MapModelFactory(FactoryBaseClass):
	def __init__(self, width, height, mapGenerationController):
		self.width = width
		self.height = height
		self.mapGenerationController = mapGenerationController
		self.generatedMapModel = None

	def generate_new_map(self):
		emptyMap = MapModel(
			self.get_copy(self.width), 
			self.get_copy(self.height)
		)
		additionController = AdditionController(emptyMap)

		mapGeneratorEngine = MapGeneratorEngine(
			Autoconnect(),
			additionController
		)

		self.generatedMapModel = self.mapGenerationController(
			self.get_copy(self.width), 
			self.get_copy(self.height),
			mapGeneratorEngine
		).generateMap()

		return self.generatedMapModel

