#!/usr/bin/env python3
import tcod

from input_handlers import EventHandler
from entity import Entity
from engine import Engine

def main() -> None:
    screen_width = 80
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    #receive events and process them
    event_handler = EventHandler()

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
    entities = {npc, player}
    engine = Engine(entities=entities, event_handler=event_handler, player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            #root_console.print(x=player.x, y=player.y, string=player.char, fg=player.color)
            engine.render(console=root_console, context=context)

            #context.present(root_console)
            events = tcod.event.wait()
            engine.handle_events(events)
            #root_console.clear() #clear leftover @

            """for event in tcod.event.wait():
                #send event to ev_keydown() and return Action
                action = event_handler.dispatch(event)
                #handling no action
                if action is None:
                    continue
                #if action is instance of MovementAction, move @ symbol
                if isinstance(action, MovementAction):
                    player.move(dx=action.dx, dy=action.dy)
                elif isistance(action, EscapeAction):
                    raise SystemExit()"""

if __name__ == "__main__":
    main()