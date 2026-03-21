import tile_types
import random
import tcod

from typing import Tuple, Iterator, List, TYPE_CHECKING
from game_map import GameMap
from __future__ import annotations

if TYPE_CHECKING:
    from entity import Entity


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

    def intersects(self, other: RectangularRoom) -> bool:
        """"Return True if this room overlaps with another RectangularRoom"""
        return {
            # pretty much if the area between x-y coordinates overlap return True
            other.x2 >= self.x1
            and self.x2 >= other.x1
            and other.y2 >= self.y1
            and self.y2 >= other.y1
        }

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

# def generate_dungeon(map_width, map_height) -> GameMap:
#     dungeon = GameMap(map_width, map_height)

#     # Generate 2 rooms on map
#     room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
#     room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

#     # Fill rooms up with walkable tiles
#     dungeon.tiles[room_1.inner] = tile_types.floor
#     dungeon.tiles[room_2.inner] = tile_types.floor

#     # Generate tunnel between 2 rooms
#     for x, y in tunnel_between(room_2.center, room_1.center):
#         dungeon.tiles[x, y] = tile_types.floor

#     return dungeon

def generate_dungeon(max_rooms: int, room_min_size: int, room_max_size: int,
    map_width: int, map_height: int, player: Entity,
) -> GameMap:
    """Generate new dungeon map"""
    dungeon = GameMap(map_width, map_height)

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        # Subtract 1 to account for walls
        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)
        # RectangularRoom class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue    # room inersects, go to next attempt
        # If no intersections, then room works

        # Dig out rooms inner area
        dungeon.tiles[new_room.inner] = tiles_types.floor
        if len(rooms) == 0: # The starting room for the player
            player.x, player.y = new_room.center
        else:   # All rooms after first
            #Dig out tunnel between this room and previous one
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor
        
        # Lastly, append new room to list
        rooms.append(new_room)

    return dungeon