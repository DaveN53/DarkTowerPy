import random

from darktower.dt_game_display import DTGameDisplay
from darktower.enums import InventoryItems


def decide_winnings(game_display: DTGameDisplay, odds: float = 1.0):
    rewards = []
    rewarded_gold = random.randrange(0, 20)
    game_display.current_gold += rewarded_gold
    rewards.append(InventoryItems.GOLD)

    random_item = random.randrange(0, 100)
    if random_item <= 5 * odds:
        game_display.current_items[InventoryItems.WIZARD] = True
        rewards.append(InventoryItems.WIZARD)
    elif random_item <= 10 * odds:
        game_display.current_items[InventoryItems.PEGASUS] = True
        rewards.append(InventoryItems.PEGASUS)
    elif random_item <= 20 * odds:
        game_display.current_items[InventoryItems.SWORD] = True
        rewards.append(InventoryItems.SWORD)
    elif random_item <= 50 * odds:
        key = game_display.attempt_award_key()
        if key:
            rewards.append(key)

    return rewards
