import pygame



class Player:
    def __init__(self, faction):
        self.money = 10
        self.faction = faction

        # PLAYERS.append(self)

    def new_round(self):
        self.money += 10
        print(f"Player {self.faction}: {self.money}")

    def spend(self, amount):
        self.money -= amount
        print(f"Spent: {amount}| Now left: {self.money}")

    def enough_money(self, cost):
        if cost <= self.money:
            # print("Can buy this")
            return True
        else:
            print("Cannot buy this")
            return False

PLAYERS = [Player(1), Player(2)]

if __name__ == "__main__":
    print("dont run this as main")