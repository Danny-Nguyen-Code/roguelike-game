import tile_types
import random
import tcod

from typing import Tuple, Iterator
from game_map import GameMap


class RectangularRoom:
    # Takes x,y coordinates of top left corner and computes coordinates of bottom
    # left corner
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        """Read-only variable for class that describes x,y coordinates of the
        center of the room
        """
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return inner area of this room as a 2D array index"""
        # Add + 1 to self.x1 and self.x2 to account for a wall separating rooms
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

def tunnel_between(
    start: Tuple[int, int],end: Tuple[int, int]
    ) -> Iterator[Tuple[int, int]]:
        """Return an L-shaped tunnel between these two points.
        Input: 2 Tuples with 2 ints each
        Output: Iterator of Tuple of 2 ints, all Tuples will be x-y coordinates"""
        # Grab coordinates out of Tuples
        x1, y1 = start
        x2, y2 = end
        if random.random() < 0.5:   # 0.5 probability
            # Move horizonatlly, then vertically
            corner_x, corner_y = x2, y1
        else:
            # Move vertically, then horizontally
            corner_x, corner_y = x1, y2
        
        # Generate coordinates for this tunnel
        # Bresenham lines = line-of-sight line, useful for getting line from A->B
        # Get 2 lines, to reate an L-shaped tunnel
        # Yield returns a generator - which returns a value, but keeps local state
        # allowing the function to pick up where it left off when called again
        for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
            yield x, y
        for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
            yield x, y

def generate_dungeon(map_width, map_height) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
    room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

    dungeon.tiles[room_1.inner] = tile_types.floor
    dungeon.tiles[room_2.inner] = tile_types.floor

    for x, y in tunnel_between(room_2.center, room_1.center):
        dungeon.tiles[x, y] = tile_types.floor

    return dungeon