from copy import deepcopy

# XXX remove this, immutability doesn't really help things
class FactoryBaseClass():
    def get_copy(self, val):
        return deepcopy(val)
