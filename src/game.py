from grid import Grid
from player import Player
from entity import Entity

player = Player()
grid = Grid()

grid.set_player(player)
grid.make_outer_walls()
grid.add_random_l_walls()
grid.randomize_items()

command = "a"
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    grid.print_status(player.score)
    command = input("Use WASD to move, I for inventory, Q/X to quit. ")
    command = command.casefold()[:1]

    # Visa inventory
    if command == "i":
        player.show_inventory()

    # Dictionary med bokstav kopplad till riktning x och y
    directions = {
        "a": (-1, 0),   # Vänster
        "d": (1, 0),    # Höger
        "w": (0, -1),   # Upp
        "s": (0, 1)     # Ner
    }

    if command in directions:
        x, y = directions[command]

        # Vad finns i rutan dit spelaren vill gå
        target_x = player.pos_x + x
        target_y = player.pos_y + y
        target_item = grid.get(target_x, target_y)

        # Fråga spelaren: "Är det okej att gå hit?"
        if player.can_move(target_item, target_x, target_y, grid):

            # Stegräknare - efter något plockats upp, kan man gå 5 steg
            # utan att det dras några poäng.
            if player.grace_period > 0:
                player.grace_period -= 1
            else:
                player.score -= 1

            # Om det var ett annat föremål (mat/fälla/nyckel), kör dess interact
            if isinstance(target_item, Entity):
                target_item.interact(player, grid, target_x, target_y)

            # Flytta spelaren
            player.move(x, y)

            # Stegräknare - efter 25 steg så slumpas en ny consumable på spelplanen
            # Välj något slumpmässig ätbart från den befintliga pickups-listan
            player.fertile_soil += 1
            if player.fertile_soil == 25:
                name = grid.spawn_random_consumable()
                print(f"🌱 A new {name} grew from the fertile soil!")
                player.fertile_soil = 0

            # Finns poäng kvar för att ta ett steg till eller ska spelet avslutas
            if player.score <= 0:
                print("\nYour score is 0 and you loose :(")
                break


# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")
