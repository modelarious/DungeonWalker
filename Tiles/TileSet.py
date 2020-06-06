#from Tiles import *
from AnchorTile import AnchorTile
from BlockedTile import BlockedTile
from GoalTile import GoalTile
from PassableTile import PassableTile
from PlayerTile import PlayerTile
from StartTile import StartTile
from TempPathTile import TempPathTile

charSet = {
        "anchor": AnchorTile(),
        "blocked": BlockedTile(),
        "goal": GoalTile(),
        "passable": PassableTile(),
        "player": PlayerTile(),
        "pathTemp": TempPathTile(),
        "start": StartTile(),
}

print(charSet)
