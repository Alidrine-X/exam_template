import random
import time
from entity import Wall, Key, Chest, Bomb, pickups, traps, tools, bombs


class Grid:
    """Representerar spelplanen. Du kan ändra standardstorleken och tecknen för olika rutor. """
    width = 36
    height = 12
    empty = "."  # Tecken för en tom ruta
    wall = "■"   # Tecken för en ogenomtränglig vägg
    blast = "X"

    def __init__(self):
        """Skapa ett objekt av klassen Grid"""
        # Spelplanen lagras i en lista av listor. Vi använder "list comprehension" för att
        # sätta tecknet för "empty" på varje plats på spelplanen.
        self.data = [[self.empty for y in range(self.width)] for z in range(
            self.height)]


    def get(self, x, y):
        """Hämta det som finns på en viss position. Returnera vägg om det är utanför spelplanen"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.data[y][x]

        return Wall("Outer Wall", "█", destructible=False)

    def set(self, x, y, value):
        """Ändra vad som finns på en viss position"""
        self.data[y][x] = value

    def set_player(self, player):
        self.player = player

        # Vi börjar med att titta på mitten av grid:en
        target_x = self.width // 2
        target_y = self.height // 2

        # Om det inte är tomt i mitten, letar vi efter närmsta lediga ruta
        # Vi letar i en fyrkant som blir större och större (offset 0, 1, 2...)
        found = False
        for offset in range(0, 10):
            for dx in range(-offset, offset + 1):
                for dy in range(-offset, offset + 1):
                    # Testa en ny koordinat nära mitten
                    test_x = target_x + dx
                    test_y = target_y + dy

                    # Kontroll om rutan är tom för placering av spelare
                    if self.is_empty(test_x, test_y):
                        self.player.pos_x = test_x
                        self.player.pos_y = test_y
                        found = True
                        break  # Avbryt innersta loopen
                if found: break  # Avbryt nästa loop
            if found: break  # Avbryt yttersta loopen

    def clear(self, x, y):
        """Ta bort item från position"""
        self.set(x, y, self.empty)

    def __str__(self):
        """Gör så att vi kan skriva ut spelplanen med print(grid)"""
        xs = ""
        for y in range(len(self.data)):
            row = self.data[y]
            for x in range(len(row)):
                if x == self.player.pos_x and y == self.player.pos_y:
                    xs += "@"
                else:
                    xs += str(row[x])
            xs += "\n"
        return xs

    def make_outer_walls(self):
        """Skapar oförstörbara ytterväggar runt hela spelplanen"""
        # Vertikala väggar (vänster och höger sida)
        for i in range(self.height):
            self.set(0, i, Wall("Outer Wall", "█", destructible=False))
            self.set(self.width - 1, i, Wall("Outer Wall", "█", destructible=False))

        # Horisontella väggar (topp och botten)
        for j in range(1, self.width - 1):
            self.set(j, 0, Wall("Outer Wall", "█", destructible=False))
            self.set(j, self.height - 1, Wall("Outer Wall", "█", destructible=False))

    def add_random_l_walls(self, count=2):
        """Placerar ut 'count' antal L-formade väggar på slumpmässiga platser."""
        for _ in range(count):
            # 1. Slumpa en startpunkt (undvik ytterväggarna)
            # Vi lämnar marginal (4 steg) så att L-formen får plats
            start_x = random.randint(2, self.width - 5)
            start_y = random.randint(2, self.height - 3)

            # 2. Slumpa riktning (vänster/höger och upp/ner)
            dir_x = random.choice([-1, 1])
            dir_y = random.choice([-1, 1])

            # 3. Rita den horisontella delen (3-4 block lång)
            length = random.randint(3, 7)
            for i in range(length):
                x = start_x + (i * dir_x)
                # Vi kollar is_empty och player så vi inte skriver över andra saker
                if self.is_empty(x, start_y):
                    self.set(x, start_y, Wall("Inner Wall", "■", destructible=True))

            # 4. Rita den vertikala delen (2-3 block lång)
            height = random.randint(2, 3)
            for j in range(1, height + 1):
                y = start_y + (j * dir_y)
                if self.is_empty(start_x, y):
                    self.set(start_x, y, Wall("Inner Wall", "■", destructible=True))

    # Används i filen pickups.py
    def get_random_x(self):
        """Slumpa en x-position på spelplanen"""
        return random.randint(0, self.width-1)

    def get_random_y(self):
        """Slumpa en y-position på spelplanen"""
        return random.randint(0, self.height-1)

    def is_empty(self, x, y):
        """Returnerar True om det inte finns något på aktuell ruta"""

        # Kolla yttre gränser (förhindra krasch)
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        # Kolla om väggar/items
        if self.data[y][x] != self.empty:
            return False

        # Kolla spelaren (om spelaren har skapats än)
        if hasattr(self, 'player') and self.player is not None:
            if x == self.player.pos_x and y == self.player.pos_y:
                return False  # Spelaren står här, alltså inte "empty"

        return True  # Hittade inget hinder!

    def print_status(self, score):
        """Visa spelvärlden och antal poäng."""
        print("--------------------------------------")
        print(f"You have {score} points.")
        print(self)

    def place_items_from_list(self, item_list):
        for item in item_list:
            while True:
                # Slumpa en position tills vi hittar en som är ledig
                x = self.get_random_x()
                y = self.get_random_y()
                if self.is_empty(x, y) and (x != self.player.pos_x or y != self.player.pos_y):
                    self.set(x, y, item)
                    break

    def randomize_items(self):
        """Huvudfunktion som placerar ut allt i spelet."""
        self.place_items_from_list(pickups)
        self.place_items_from_list(traps)
        self.place_items_from_list(tools)
        self.place_items_from_list(bombs)

        # Skapa 3 kistor och 3 matchande nycklar
        for i in range(3):
            key = Key(f"Key {i + 1}", "k", 0)
            chest = Chest(f"Chest {i + 1}", "C", 100)  # Varje kista ger 100 poäng

            self.place_items_from_list([key])
            self.place_items_from_list([chest])

    def spawn_random_consumable(self):
        """Väljer ut EN slumpmässig grönsak från listan och placerar på griden."""
        # Välj ett objekt-template från den importerade listan 'pickups'
        new_pickup = random.choice(pickups)

        # Skicka föremålet i en lista för utplacering i grid
        self.place_items_from_list([new_pickup])

        # Returnera namnet så att game.py kan skriva ut det
        return new_pickup.name

    def update_world(self, player):
        if player.fertile_soil >= 25:
            name = self.spawn_random_consumable()
            print(f"🌱 A new {name} grew from the fertile soil!")
            player.fertile_soil = 0

    def detonate_bomb(self, player):
        for y in range(self.height):
            for x in range(self.width):

                # Bomben har hittats, rensa 3 x 3 rutor
                if isinstance(self.get(x, y), Bomb):
                    print("\n💥 TICK... TICK... BOOM!")

                    # Rita ut explosionen först i 3x3
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            self.set(x + dx, y + dy, self.blast)

                    print(self)  # Skriv ut grid så spelaren ser explosionen
                    time.sleep(0.5)  # Pausa i en halv sekund så man hinner se!

                    # Faktisk rensning i 3x3
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            self.clear(x + dx, y + dy)

                    # Spelaren stod i vägen
                    if abs(player.pos_x - x) <= 1 and abs(player.pos_y - y) <= 1:
                        print("Aargh! You got caught in the blast wave!")
                        player.score -= 20  # Eller dör spelaren direkt?

                    return  # Vi hittade och sprängde bomben, vi kan sluta leta

