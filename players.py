import pygame

COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "gray": (225, 225, 225),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "dark gray": (25, 25, 25),
    "light blue": (173, 216, 230),
}

class Player:
    def __init__(self, faction):
        self.money = 10
        self.faction = faction
        if self.faction == 1:
            self.color = COLORS["blue"]
        else:
            self.color = COLORS["red"]
        # PLAYERS.append(self)

    def new_round(self):
        self.money += 10
        self.money += int(self.money*0.1)

    def spend(self, amount):
        self.money -= amount

    def enough_money(self, cost):
        if cost <= self.money:
            return True
        else:
            return False

PLAYERS = [Player(1), Player(2)]

if __name__ == "__main__":
    print("dont run this as main")