from grid import Grid
from player import Player
from entity import Wall, Entity

grid = Grid()
player = Player()

grid.make_outer_walls()
grid.add_random_l_walls()
grid.set_player(player)
grid.randomize_items()

command = "a"
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    grid.print_status(player.score)
    command = input("Use WASD to move, I for inventory, Q/X to quit. ")
    command = command.casefold()[:2]

    # Visa inventory
    if command == "i":
        player.show_inventory()

    # Dictionary med bokstav kopplad till riktning x och y
    # J framför ger två steg i angiven riktning
    directions = {
        "a": (-1, 0),   # Vänster
        "d": (1, 0),    # Höger
        "w": (0, -1),   # Upp
        "s": (0, 1)    # Ner
    }

    if command in directions:
        x, y = directions[command]

        # Vad finns i rutan dit spelaren vill gå
        target_x = player.pos_x + x
        target_y = player.pos_y + y
        target_item = grid.get(target_x, target_y)
        print(f"Här är kommandot {command} {target_item} {target_x} {target_y}")

        # Är nästa steg en vägg,
        # yttervägg kräver ny input, innervägg kräver spade eller ny input
        if isinstance(target_item, Wall):
            if not target_item.try_to_demolish(player, grid, target_x, target_y):
                continue

        # Är nästa steg något ätbart, en fälla, kista eller nyckel
        elif isinstance(target_item, Entity):
            target_item.interact(player, grid, target_x, target_y) # Kör effekten

        # Flytta spelare, uppdatera poäng och antal steg för bördig jord
        player.move(x, y)
        player.move_points()
        grid.update_world(player)

        # Finns poäng kvar för att ta ett steg till eller ska spelet avslutas
        if not player.is_alive():
            print("\nYour score is 0 and you lose :(")
            break


# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")
