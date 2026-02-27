class Player:
    marker = "@"

    def __init__(self, x=None, y=None):
        self.pos_x = x
        self.pos_y = y
        self.score = 10
        self.grace_period = 0
        self.fertile_soil = 0
        self.inventory = []

    # Flyttar spelaren. "dx" och "dy" är skillnaden
    def move(self, dx, dy):
        """Flyttar spelaren.\n
        dx = horisontell förflyttning, från vänster till höger\n
        dy = vertikal förflyttning, uppifrån och ned"""
        self.pos_x += dx
        self.pos_y += dy

    def show_inventory(self):
        print(f"Your inventory: {', '.join([item.name for item in self.inventory])}")

    def can_move(self, target_item, target_x, target_y, grid):

        # Om det är en vägg, låt väggen avgöra om spelaren får passera (interact returnerar True/False)
        from entity import Wall
        if isinstance(target_item, Wall):
            return target_item.interact(self, grid, target_x, target_y)

        # För allt annat (empty, pickups, traps) är svaret True
        return True



