from darktower.enums import InventoryItems


class Player:
    def __init__(self):
        self.gold = 100
        self.frontier = 1
        self.items = {
            InventoryItems.WARRIOR: 10,
            InventoryItems.FOOD: 25,
            InventoryItems.SCOUT: False,
            InventoryItems.HEALER: False,
            InventoryItems.BEAST: False,
            InventoryItems.SWORD: False,
            InventoryItems.BRASS_KEY: False,
            InventoryItems.SILVER_KEY: False,
            InventoryItems.GOLD_KEY: False
        }

    def update_frontier(self):
        if self.frontier < 4:
            self.frontier += 1

    def check_starvation(self):
        """
        Alert if starving
        - when only 4 turns of food left
        Remove 1 warrior if food is 0
        :return:
        """
        if (self.items[InventoryItems.FOOD] / self.get_food_per_turn()) <= 4:
            if self.items[InventoryItems.FOOD] == 0:
                self.items[InventoryItems.WARRIOR] = max(self.items[InventoryItems.WARRIOR] - 1, 1)
            return True
        return False

    def update_food(self):
        self.items[InventoryItems.FOOD] = max(self.items[InventoryItems.FOOD] - self.get_food_per_turn(), 0)

    def get_food_per_turn(self):
        return max((self.items[InventoryItems.WARRIOR] - 1) / 15, 1)

    def update_item(self, item: InventoryItems, count: int):
        if item in (InventoryItems.WARRIOR, InventoryItems.FOOD):
            self.items[item] += count
        else:
            self.items[item] = bool(count)
