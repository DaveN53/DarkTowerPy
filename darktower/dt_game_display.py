import pygame

from darktower.enums import DTEvent, InventoryItems, DTUserEvent
from darktower.player import Player


class DTGameDisplay:
    def __init__(self):
        self.width = 320
        self.height = 240
        self.current_event = None
        pygame.init()
        self.game = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Dark Tower')
        self.difficulty = None
        self.players = []
        self.c_player: Player = None

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
        return self.c_player.gold

    @property
    def current_items(self):
        return self.c_player.items

    def attempt_purchase(self, price: int, item: InventoryItems, item_count: int):
        player = self.players[self.current_player]
        if price > player.gold:
            return pygame.event.Event(DTUserEvent.DT_SELECTION,
                                      {'dt_event': DTEvent.BAZAAR_CLOSED})
        else:
            if (item not in (InventoryItems.FOOD, InventoryItems.WARRIOR)) and self.current_items[item]:
                return pygame.event.Event(DTUserEvent.DT_SELECTION,
                                          {'dt_event': DTEvent.SHOW_INVENTORY,
                                           'item': item})
            player.gold -= price
            player.update_item(item, item_count)
            return pygame.event.Event(DTUserEvent.DT_SELECTION,
                                      {'dt_event': DTEvent.SHOW_INVENTORY,
                                       'item': item})



