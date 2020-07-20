from models.MapModel import NeighborOffsets
from settings import charSet
from TileMapping.TileType import TileType
from TileMapping.TileLoader import Same, Different

def element_is_not_in(x, arr):
    return x not in arr

def element_is_in(x, arr):
    return x in arr

class TileMapper:
    def __init__(self, tileLoader):
        self._tileLoader = tileLoader # XXX could be changed to a TileLoaderFactory later -> subclass RandomTileSetLoaderFactory that gives a random tileset
        self._pointToTileMap = {} # mapping of (x, y) to the tile that should be in that space XXX that's not true
    
	# Tile mapper asks Map Model to get neighbors, then builds a key up of 
    # similar neighbors and neighbors that are different, then asks 
    # tileLoader what tile to use there and stores it for later retrieval
    def process_board(self, mapModel):
        print("processing tileset")

        self._pointToTileMap = {} 
        for point in mapModel:
            
            x, y = point
            neighbs = mapModel.get_all_eight_surrounding_neighbors_and_self(point)

            # based on the center tile, choose which tile type to use
            # XXX begging for objects to encompass this config and the
            # key building process
            blockedChars = [charSet["blocked"]]
            if neighbs[1][1] in blockedChars:
                # if the middle tile is blocked, then SAME tiles will be in blockedChars
                existenceFunc = element_is_in
                tileType = TileType.WALL
            else:
                # if the middle tile is passable, then SAME tiles will NOT be in blockedChars
                existenceFunc = element_is_not_in
                tileType = TileType.GROUND

            # build a key like the following to use to get the correct pokemon tile:
            '''
            exampleKey = (
                (Different, Different, Different),
                (Same,      Same,      Different),
                (Same,      Same,      Different)
            )
            '''
            tileLoaderKey = []
            for yDim in range(len(neighbs)):
                tileLoaderRow = []
                for xDim in range(len(neighbs[yDim])):
                    if existenceFunc(neighbs[yDim][xDim], blockedChars):
                        tileLoaderRow.append(Same)
                    else:
                        tileLoaderRow.append(Different)
                tileLoaderKey.append(tuple(tileLoaderRow))
            
            tileLoaderKey = tuple(tileLoaderKey)

            self._pointToTileMap[(x,y)] = self._tileLoader.get_tile(tileType, tileLoaderKey)

        print("done processing tileset")
    
    def get_tile_mapping(self):
        return self._pointToTileMap.items()

# going to need two objects at least:
# - object that handles loading all the tiles from a tileset file -> TileLoader
# - object that handles reading in the map, mapping the correct tiles to the 
#   right positions and holding that result in a 2d array, of which a XXX 2x2 
#   box of tiles can be selected to be returned (step towards the camera feature) -> TileMapper