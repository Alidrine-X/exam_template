import random
from src.objects import Wall

class Grid:
    """Representerar spelplanen. Du kan ändra standardstorleken och tecknen för olika rutor. """
    width = 36
    height = 12
    empty = "."  # Tecken för en tom ruta
    wall = "■"   # Tecken för en ogenomtränglig vägg
    blast = "X"


    def __init__(self):
        """Skapa ett objekt av klassen Grid. Spelplanen lagras i en lista av listor.
        Vi använder "list comprehension" för att sätta tecknet för "empty" på varje
        plats på spelplanen."""
        self.data = [[self.empty for y in range(self.width)] for z in range(
            self.height)]
        self.player = None
        self.edibles_left = 0


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


    def get(self, x, y):
        """Hämta det som finns på en viss position. Returnera vägg om det är utanför spelplanen"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.data[y][x]

        return Wall("Outer Wall", "█", destructible=False)


    def set(self, x, y, value):
        """Placerar ett objekt på en specifik koordinat i spelvärlden"""
        self.data[y][x] = value


    def clear(self, x, y):
        """Ta bort item från position på spelplanen av något som plockats upp och sätt empty """
        self.set(x, y, self.empty)


    def print_status(self, score):
        """Visa spelvärlden och antal poäng."""
        print("--------------------------------------")
        print(f"You have {score} points.")
        print(self)


    def get_random_x(self):
        """Slumpa en x-position på spelplanen"""
        return random.randint(0, self.width-1)


    def get_random_y(self):
        """Slumpa en y-position på spelplanen"""
        return random.randint(0, self.height-1)


    def is_empty(self, x, y):
        """Kontrollerar om en ruta är ledig från både föremål och spelare"""

        # Kolla yttre gränser av grid
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        # Kolla om väggar/items
        if self.data[y][x] != self.empty:
            return False

        # Kolla om spelaren står här, alltså inte "empty"
        if self.player is not None and x == self.player.pos_x and y == self.player.pos_y:
                return False

        return True  # Hittade inget hinder

