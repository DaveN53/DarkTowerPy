import pygame

from darktower.enums import DTEvent, InventoryItems, DTUserEvent
from darktower.player import Player


class DTGameDisplay:
    def __init__(self):
        self.width = 640
        self.height = 480
        self.current_event = None
        pygame.init()
        self.game = pygame.display.set_mode(size=(self.width, self.height))  #, flags=pygame.FULLSCREEN)
        self.width, self.height = pygame.display.get_surface().get_size()
        print('Screen Size: {} x {}'.format(self.width, self.height))
        pygame.display.set_caption('Dark Tower')
        self.difficulty = None
        self.players = []
        self.c_player = None
        self.dragon = {InventoryItems.WARRIOR: 0, InventoryItems.GOLD: 0}

    @property
    def num_players(self):
        return len(self.players)

    @num_players.setter
    def num_players(self, num):
        for _ in range(num):
            self.players.append(Player())
        self.c_player = self.players[0]

    @property
    def current_player(self):
        return self.players.index(self.c_player)

    @current_player.setter
    def current_player(self, pos: int):
        self.c_player = self.players[pos]

    def end_turn(self):
        next_pos = self.current_player + 1
        if next_pos >= self.num_players:
            next_pos = 0

        self.current_player = next_pos

    @property
    def current_gold(self):
        return self.current_items[InventoryItems.GOLD]

    @current_gold.setter
    def current_gold(self, gold):
        self.current_items[InventoryItems.GOLD] = gold

    @property
    def current_warriors(self):
        return self.current_items[InventoryItems.WARRIOR]

    @current_warriors.setter
    def current_warriors(self, warriors):
        warriors = max(1, warriors)
        self.current_items[InventoryItems.WARRIOR] = warriors

    @property
    def current_items(self):
        return self.c_player.items

    def attempt_award_key(self):
        if not self.current_items[InventoryItems.BRASS_KEY] and self.c_player.frontier == 2:
            self.current_items[InventoryItems.BRASS_KEY] = True
            return InventoryItems.BRASS_KEY
        elif not self.current_items[InventoryItems.SILVER_KEY] and self.c_player.frontier == 3:
            self.current_items[InventoryItems.SILVER_KEY] = True
            return InventoryItems.SILVER_KEY
        elif not self.current_items[InventoryItems.GOLD_KEY] and self.c_player.frontier == 4:
            self.current_items[InventoryItems.GOLD_KEY] = True
            return InventoryItems.GOLD_KEY

    def attempt_purchase(self, price: int, item: InventoryItems, item_count: int):
        player = self.players[self.current_player]
        if price > self.current_gold:
            return pygame.event.Event(DTUserEvent.DT_SELECTION,
                                      {'dt_event': DTEvent.BAZAAR_CLOSED})
        else:
            if (item not in (InventoryItems.FOOD, InventoryItems.WARRIOR)) and self.current_items[item]:
                return pygame.event.Event(DTUserEvent.DT_SELECTION,
                                          {'dt_event': DTEvent.SHOW_INVENTORY,
                                           'items': [item]})
            self.current_gold -= price
            player.update_item(item, item_count)
            return pygame.event.Event(DTUserEvent.DT_SELECTION,
                                      {'dt_event': DTEvent.SHOW_INVENTORY,
                                       'items': [item, InventoryItems.GOLD]})



