from copy import deepcopy

class FactoryBaseClass():
    def get_copy(self, val):
        return deepcopy(val)
