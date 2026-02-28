import entity
from grid import Grid
from player import Player
from entity import Entity, Wall, Trap, Bomb

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
    command = input("Use WASD to move, I for inventory, Q/X to quit. ").lower()
    command = command.casefold()[:2]

    # Visa spelarens inventory
    if command == "i":
        player.show_inventory()

    # Desarmera en fälla
    if command == "t":
        current_item = grid.get(player.pos_x, player.pos_y)

        # Spelarens nuvarande position måste vara på fällan
        if isinstance(current_item, Trap):
            current_item.disarm(grid, player.pos_x, player.pos_y)
        else:
            print(f"You need to stand on a trap to remove it.")

    # Placera ut en bomb
    if command == "b":
        bomb = next((i for i in player.inventory if getattr(i, 'can_explode', False)), None)

        # Om bomb finns i inventory, spelare inte är för nära väggen så tänd stubinen
        if bomb:
            if (1 < player.pos_x < grid.width - 2) and (1 < player.pos_y < grid.height - 2):
                player.bomb_timer = 1
                bomb.symbol = "*"
                grid.set(player.pos_x, player.pos_y, bomb)
                player.inventory.remove(bomb)
                print(f"Now you have placed the bomb and lit the fuse.")
            else:
                print(f"You are to close to the wall, you got to move to place the bomb.")
        else:
            print(f"There is no bomb in your inventory, you have to pick it up first.")


    # Vill spelaren gå ett eller två steg
    if command.startswith("j") and len(command) > 1:
        move_count = 2
        direction_key = command[1]
    else:
        move_count = 1
        direction_key = command

    # Dictionary med bokstav kopplad till riktning x och y
    # J framför ger två steg i angiven riktning
    directions = {
        "a": (-1, 0),   # Vänster
        "d": (1, 0),    # Höger
        "w": (0, -1),   # Upp
        "s": (0, 1)    # Ner
    }

    # Kontrollera om riktningen är giltig
    if direction_key in directions:
        dx, dy = directions[direction_key]

        # Kolla vad som finns på första steget
        step1_x = player.pos_x + dx
        step1_y = player.pos_y + dy
        step1_item = grid.get(step1_x, step1_y)

        # Man kan aldrig hoppa ÖVER en vägg
        if move_count == 2 and isinstance(step1_item, Wall):
            print("Vägen är blockerad, du kan inte hoppa över väggar!")
            continue

        # Slutdestinationen blir ett eller två steg i angiven riktning
        target_x = player.pos_x + (dx * move_count)
        target_y = player.pos_y + (dy * move_count)
        target_item = grid.get(target_x, target_y)

        # Hantera om destinationen är en vägg, om yttervägg stå kvar
        # om innervägg kontrollera om spade finns annars stå kvar
        can_move = True
        if isinstance(target_item, Wall):
             if not target_item.try_to_demolish(player, grid, target_x, target_y):
                can_move = False  # Stoppa flytten om väggen står kvar

        # Flytta och dra poäng efter antal flyttade steg
        if can_move:
            player.pos_x = target_x
            player.pos_y = target_y

            for _ in range(move_count):
                player.move_points()

            # Lägg in i inventory om det ska sparas, justera poäng
            if isinstance(target_item, Entity):
                target_item.interact(player, grid, target_x, target_y)

            # Uppdatera antal steg för bördig jord och nytt ätbart
            grid.update_world(player)

            # Bombens stubin har brunnit ut
            if player.bomb_timer == 4:
                grid.detonate_bomb(player)
                player.bomb_timer = 0

        # Avsluta spelet om poängen är slut
        if not player.is_alive():
            print("\nYour score is 0 and you lose :(")
            break


# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")
