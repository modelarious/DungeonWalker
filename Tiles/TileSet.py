from Tiles.AnchorTile import AnchorTile
from Tiles.BlockedTile import BlockedTile
from Tiles.GoalTile import GoalTile
from Tiles.PassableTile import PassableTile
from Tiles.PlayerTile import PlayerTile
from Tiles.StartTile import StartTile
from Tiles.TempPathTile import TempPathTile

charSet = {
        "anchor": AnchorTile(),
        "blocked": BlockedTile(),
        "goal": GoalTile(),
        "passable": PassableTile(),
        "player": PlayerTile(),
        "pathTemp": TempPathTile(),
        "start": StartTile(),
}
