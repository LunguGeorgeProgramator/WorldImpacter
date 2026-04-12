
class Shop:

    def __init__(self, player):
        self.player = player
        self.transaction_status = True
        self.healing_potion = "healing_potion"
        self.healing_potion_inventory_id = 1
        self.number_of_healing_potion = 10
        self.healing_potion_price = 10
        self.flower_attack = "flower_attack"
        self.flower_attack_inventory_id = 2
        self.flower_attack_price = 5
        self.number_of_flower_attack = 10

    def sell_healing_potion(self):
        self.number_of_healing_potion -= 1

    def sell_flower_attack(self):
        self.number_of_flower_attack -= 1

    def make_buy_transaction(self, coins, sell_item):
        self.transaction_status = True
        if sell_item == self.healing_potion and coins >= self.healing_potion_price and self.number_of_healing_potion > 0:
            self.sell_healing_potion()
            coins = coins - self.healing_potion_price
            self.player.player_inventory.add_to_inventory(self.healing_potion, 1)
        elif sell_item == self.flower_attack and coins >= self.flower_attack_price and self.number_of_flower_attack > 0:
            self.sell_flower_attack()
            coins = coins - self.flower_attack_price
            self.player.player_inventory.add_to_inventory(self.flower_attack, 1)
        else:
            self.transaction_status = False
        return coins

    def restock_shop_inventory(self):
        self.number_of_healing_potion = 10
        self.number_of_flower_attack = 10