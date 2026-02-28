class Entity:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def interact(self, player, grid, target_x, target_y):
        """Standardinteraktion: gör ingenting"""
        pass

    def __str__(self):
        return self.symbol

# Ätbart som plockas upp och läggs i inventory och ger spelare gratis steg
class Consumable(Entity):
    def __init__(self, name, symbol, points):
        super().__init__(name, symbol)
        self.points = points

    def interact(self, player, grid, target_x, target_y):
        player.score += self.points
        player.inventory.append(self)
        player.grace_period = 5
        grid.clear(target_x, target_y)  # Tas bort från grid
        print(f"You found a {self.name} and got {self.points} points!")


# Verktyg som plockas upp läggs i inventory och kan användas till att ta bort innervägg
# Den tas bort när den använts
class Tool(Entity):
    def __init__(self, name, symbol, points):
        super().__init__(name, symbol)
        self.points = points
        self.can_dig = True

    def interact(self, player, grid, target_x, target_y):
        player.inventory.append(self)
        player.grace_period = 5
        grid.clear(target_x, target_y)  # Tas bort från grid
        print(f"You found a {self.name} but got no extra points")


# Fälla som ger minuspoäng varje gång spelaren går på rutan
class Trap(Entity):
    def __init__(self, name, symbol, points):
        super().__init__(name, symbol)
        self.points = points

    def interact(self, player, grid, target_x, target_y):
        player.score -= self.points
        # grid.clear anropas INTE här -> fällan blir kvar
        print(f"Oh no, you accidentally fell into a {self.name} and got -{self.points} points.")

    def disarm(self, grid, x, y):
        grid.clear(x, y)  # Tas bort från grid
        print(f"You successfully disarmed the {self.name}")

# Skattkista som ger poäng om spelare öppnar den med en nyckel
# Den tas bort när den öppnas
class Chest(Entity):
    def __init__(self, name, symbol, points):
        super().__init__(name, symbol)
        self.points = points

    def interact(self, player, grid, target_x, target_y):
        # Leta efter första saken som kan låsa upp kistan (oberoende av namn!)
        key = next((i for i in player.inventory if getattr(i, 'can_unlock', False)), None)

        if key:
            print("You unlocked the chest!")
            player.score += self.points
            player.inventory.remove(key) # Nyckeln försvinner efter användning
            grid.clear(target_x, target_y)
        else:
            print("The chest is locked. You need a key!")


# Nyckel som plockas upp och läggs i inventory och kan låsa upp en kista
# Den tas bort när den använts
class Key(Entity):
    def __init__(self, name, symbol, points):
        super().__init__(name, symbol)
        self.points = points
        self.can_unlock = True

    def interact(self, player, grid, target_x, target_y):
        player.inventory.append(self)
        player.grace_period = 5
        grid.clear(target_x, target_y)
        print("You found a key!")

# Två typer av väggar, yttervägg som inte kan krossas och innervägg som
# kan tas bort med en spade
class Wall(Entity):
    def __init__(self, name="Wall", symbol="■", destructible=False):
        super().__init__(name, symbol)
        self.destructible = destructible

    def interact(self, player, grid, target_x, target_y):
        pass

    def try_to_demolish(self, player, grid, target_x, target_y):
        # Om väggen inte kan förstöras (yttervägg)
        if not self.destructible:
            print("Den här väggen är för massiv för att rubba.")
            return False  # Hindra flytt

        # Om det är en innervägg, leta efter spade (Tool)
        shovel = next((i for i in player.inventory if getattr(i, 'can_dig', False)), None)

        if shovel:
            print(f"Du använder din {shovel.name} och river väggen!")
            grid.clear(target_x, target_y)
            player.inventory.remove(shovel)
            return True
        else:
            print("Du behöver en spade för att komma igenom väggen.")
            return False


pickups = [
    Consumable("carrot", "?", 20),
    Consumable("apple", "?", 20),
    Consumable("strawberry", "?", 20),
    Consumable("cherry", "?", 20),
    Consumable("watermelon", "?", 20),
    Consumable("radish", "?", 20),
    Consumable("cucumber", "?", 20),
    Consumable("meatball", "?", 20)
]

traps = [
    Trap("snare", "¤", 10),
    Trap("maple door", "¤", 10),
    Trap("quicksand", "¤", 10),
    Trap("bear shears", "¤", 10),
    Trap("floor hatch", "¤", 10),
    Trap("fishing net", "¤", 10),
    Trap("fire", "¤", 10)
]

tools = [
    Tool("shovel", "!", 0),
    Tool("spade", "!", 0)
]
