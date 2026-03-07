import random
import time
from src.builder import place_items_from_list
from src.objects import Bomb, Entity, Exit, Trap, Wall, edible_templates


# ---------------------------------------------------------------------
# Funktioner som hanterar vad spelaren önskar göra och som
# avgör om spelare kan/får flytta sig
# ---------------------------------------------------------------------

# Dictionary med alla giltiga kommandon
commands = {
    "w": ("move", (0, -1), 1),  # Move up
    "a": ("move", (-1, 0), 1),  # Move left
    "s": ("move", (0, 1), 1),  # Move down
    "d": ("move", (1, 0), 1),  # Move right
    "jw": ("jump", (0, -1), 2),  # Jump up
    "ja": ("jump", (-1, 0), 2),  # Jump left
    "js": ("jump", (0, 1), 2),  # Jump down
    "jd": ("jump", (1, 0), 2),  # Jump right
    "i": ("inventory", None, None),  # Show inventory
    "t": ("trap", None, None),  # Disarm trap
    "b": ("bomb", None, None),  # Place bomb
    "e": ("exit", None, None),  # Exit as winner
    "q": ("quit", None, None),  # Quit
    "x": ("quit", None, None)  # Quit
}


def try_move_player(grid, player, dx, dy, move_count):
    """ Försöker flytta spelaren move_count steg i riktningen dx, dy.
    Returnerar True om flytten (och eventuella rivningar) genomfördes. """

    # Scanna vägen för hinder (1 eller 2 steg framåt)
    for i in range(1, move_count + 1):
        check_x = player.pos_x + (dx * i)
        check_y = player.pos_y + (dy * i)
        item = grid.get(check_x, check_y)

        if isinstance(item, Wall):

            # Försök riva väggen. Om det misslyckas stannar vi helt.
            if not item.try_to_demolish(player, grid):
                return False

    # Om vi kom hit är vägen fri (eller röjd). Genomför flytten.
    player.move(dx * move_count, dy * move_count)

    # Uppdatera poäng och bördig jord för varje steg som tagits
    for _ in range(move_count):
        player.move_points()

    # Interagera med det som finns på slutdestinationen
    final_item = grid.get(player.pos_x, player.pos_y)
    if isinstance(final_item, Entity):
        final_item.interact(player, grid, player.pos_x, player.pos_y)

    # Uppdatera världen med nytt ätbart tack vare bördig jord
    update_world(grid, player)

    return True


def try_disarm_trap(grid, player):
    """Med kommando T, tas fälla bort om spelaren står på den"""
    current_item = grid.get(player.pos_x, player.pos_y)

    # Spelarens nuvarande position måste vara på fällan
    if isinstance(current_item, Trap):
        current_item.disarm(grid, player.pos_x, player.pos_y)
    else:
        print(f"\nYou need to stand on a trap to remove it.")


def try_place_bomb(grid, player):
    """Med kommando B, placerar bomb ut på spelplanen där spelaren står"""
    bomb = next((i for i in player.inventory if getattr(i, 'can_explode', False)), None)

    # Om bomb finns i inventory, spelare inte är för nära väggen så tänd stubinen
    if bomb:
        if (1 < player.pos_x < grid.width - 2) and (1 < player.pos_y < grid.height - 2):
            player.bomb_timer = 1   # Start timer (1 = bomb placed, explosion after >=4)
            bomb.symbol = "*"
            bomb.placed = True
            grid.set(player.pos_x, player.pos_y, bomb)
            player.inventory.remove(bomb)
            print(f"\nNow you have placed the bomb and lit the fuse.")
        else:
            print(f"\nYou are to close to the wall, you got to move to place the bomb.")
    else:
        print(f"\nThere is no bomb in your inventory, you have to pick it up first.")


def try_exit_game(grid, player):
    """Med kommando E, vinner spelaren om allt ätbart från originaluppsättningen är upplockat"""
    current_item = grid.get(player.pos_x, player.pos_y)

    # Spelarens nuvarande position måste vara på E, om interact returnerar True, vinner man
    if isinstance(current_item, Exit):
        if current_item.interact(player, grid, player.pos_x, player.pos_y):
            return True
    else:
        print(f"\nYou need to stand on E to Exit.")

    return False

# ---------------------------------------------------------------------
# Metoder som körs automatiskt eller som en konsekvens av en handling
# ---------------------------------------------------------------------

def spawn_random_edible(grid, is_new):
    """Väljer ut något slumpmässig ätbart från originallistan och placerar på grid."""
    # Välj ett objekt-template från den importerade listan 'edible_templates'
    new_edible = random.choice(edible_templates)

    # Skicka föremålet i en lista för utplacering i grid
    place_items_from_list(grid,[new_edible], is_new)

    # Returnera namnet så att game_new.py kan skriva ut det
    return new_edible.name


def update_world(grid, player):
    """När spelaren tagit 25 steg läggs något nytt ätbart till. Det markeras att det är
    tillagt i efterhand med is_new"""
    if player.fertile_soil >= 25:
        is_new = True
        name = spawn_random_edible(grid, is_new)
        print(f"\n🌱 A new {name} grew from the fertile soil!")
        player.fertile_soil -= 25


def detonate_bomb(grid, player):
    """Detonerar bomb när spelaren plockat upp bomb, placerat ut bomb och gått 3 steg"""
    for y in range(grid.height):
        for x in range(grid.width):

            # Bomben har hittats, rensa 3 x 3 rutor
            if isinstance(grid.get(x, y), Bomb):
                print("\n💥 TICK... TICK... BOOM!")

                # Rita ut explosionen först i 3x3
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        grid.set(x + dx, y + dy, grid.blast)

                print(grid)  # Skriv ut grid så spelaren ser explosionen
                time.sleep(0.5)  # Pausa i en halv sekund så man hinner se!

                # Faktisk rensning i 3x3
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        grid.clear(x + dx, y + dy)

                # Spelaren stod i vägen
                if abs(player.pos_x - x) <= 1 and abs(player.pos_y - y) <= 1:
                    print("\nAargh! You got caught in the blast wave!")
                    player.score -= 20

                return  # Vi hittade och sprängde bomben, vi kan sluta leta


