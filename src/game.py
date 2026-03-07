from src.grid import Grid
from src.player import Player
from src.actions import try_move_player, try_place_bomb, detonate_bomb, try_exit_game, try_disarm_trap, commands
from src.builder import make_outer_walls, add_l_walls, set_player, randomize_items, set_exit

grid = Grid()
player = Player()

make_outer_walls(grid)
add_l_walls(grid)
set_player(grid, player)
randomize_items(grid, is_new=False)
set_exit(grid, player)


# Hanterar användarens input och styr kommunikationen
command = ""
while command not in ["q", "x"]:
    grid.print_status(player.score)
    print("Use WASD to move | J+WASD to jump | Q/X to quit")
    print("I = show inventory | T = disarm trap | B = place bomb | E = exit as a winner")

    command = input("> ").casefold()[:2]

    if command in commands:
        action, direction, steps = commands[command]

        # Spelarens förflyttning
        if action in ["move", "jump"]:
            dx, dy = direction  # Packa upp x och y från move_direction
            if try_move_player(grid, player, dx, dy, steps):
                # Bombens stubin har brunnit ut
                if player.bomb_timer >= 4:  # 3 steps after placement
                    detonate_bomb(grid, player)
                    player.bomb_timer = 0

        # Visa spelarens inventory
        elif action == "inventory":
            player.show_inventory()

        # Exit möjlig om spelaren plockat upp alla ursprungliga ätbara saker
        elif action == "exit":
            if try_exit_game(grid, player):
                command = "q"

        # Desarmera en fälla
        elif action == "trap":
            try_disarm_trap(grid, player)

        # Placera ut en bomb
        elif action == "bomb":
            try_place_bomb(grid, player)

        # Avsluta spelet
        elif action == "quit":
            break

    else:
        print(f"\nI don't understand your command: {command}")


    # Avsluta spelet om poängen är slut
    if not player.is_alive():
        print("\nYour score is 0 and you lose :(")
        break


# Hit kommer vi när while-loopen slutar
print("\nThank you for playing!")
