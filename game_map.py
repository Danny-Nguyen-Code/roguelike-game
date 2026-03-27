from __future__ import annotations

from typing import Iterable, TYPE_CHECKING

import numpy as np
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from entity import Entity

class GameMap:
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.entities = set(entities)
        # Create 2D array, filled with value of tile_types.floor to fill
        # self.tiles with floor tiles
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        # Tiles the player can currently see
        self.visible = np.full((width, height), fill_value=False, order="F")
        # Tiles the player has seen before
        self.explored = np.full((width, height), fill_value=False, order="F")        
        
    def in_bounds(self, x: int, y: int) -> bool:
        """Return true if x and y are inside of the bounds of this map, 
        used to ensure player doesn't move beyond map."""
        return self.width > x >= 0 and self.height > y >= 0

    # Renders the entire map
    def render(self, console: Console) -> None:
        # console.tiles_rgb runs faster than console.print
        # console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
        """
        Renders the map.
        If a tile is in the "visible" array, draw it with "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the
        "dark" colors.
        Otherwise, it is "SHROUD".
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )

        for entity in self.entities:
            # Print entities that are in FOV
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char,
                    fg=entity.color)