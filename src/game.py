from .grid import Grid
from .player import Player
from . import pickups


player = Player(2, 1)
score = player.score
inventory = []

g = Grid()
g.set_player(player)
g.make_walls()

g.add_two_l_walls()
pickups.randomize(g)

def print_status(game_grid, score):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"You have {score} points.")
    print(game_grid)

command = "a"
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    print_status(g, score)
    command = input("Use WASD to move, I for inventory, Q/X to quit. ")
    command = command.casefold()[:1]

    # Visa inventory
    if command == "i":
        print(f"Your inventory: {', '.join([item.name for item in inventory])}")

    # Dictionary med bokstav kopplad till riktning x och y
    directions = {
        "a": (-1, 0),   # Vänster
        "d": (1, 0),    # Höger
        "w": (0, -1),   # Upp
        "s": (0, 1)     # Ner
    }

    if command in directions:
        x, y = directions[command]

        # Vad finns i rutan om spelaren tar nästa önskade steg
        maybe_event = g.get(player.pos_x + x, player.pos_y + y)

        # Om inte vägg hittas så kan spelaren flytta sitt nästa steg
        if "■" != maybe_event:
            player.move(x, y)
            score -= 1

            # Frukt eller grönsak hittad
            if isinstance(maybe_event, pickups.Item):
                # we found something
                score += maybe_event.value
                print(f"You found a {maybe_event.name}, +{maybe_event.value} points.")
                inventory.append(maybe_event)
                #g.set(player.pos_x, player.pos_y, g.empty)
                g.clear(player.pos_x, player.pos_y)

            # Finns poäng kvar för att ta ett steg till eller ska spelet avslutas
            if score <= 0:
                command = "q"
                print("\nYour score is 0 and you loose :(")


# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")
