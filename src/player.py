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

    def move_points(self):
        """Hanterar poängavdrag (eller grace) och bördighet för ett utfört steg."""
        # 1. Hantera poäng/grace
        if self.grace_period > 0:
            self.grace_period -= 1
        else:
            self.score -= 1

        # 2. Hantera fertile soil
        self.fertile_soil += 1

    def show_inventory(self):
        print(f"Your inventory: {', '.join([item.name for item in self.inventory])}")

    def is_alive(self):
        """Returnerar True om spelaren har poäng kvar."""
        return self.score > 0
