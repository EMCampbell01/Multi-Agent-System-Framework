from collections import defaultdict
from dataclasses import dataclass


@dataclass
class InventoryItemData:
    item_count: int = 0
    item_max: int | None = None
    negatives: bool = False


class Inventory:
    
    def __init__(self) -> None:
        self.inventory: defaultdict[str, InventoryItemData] = defaultdict(InventoryItemData)

    def add_item(self, item: str, quantity: int) -> None:
        '''Adds quantity of item to inventory'''
        self.inventory[item].item_count += quantity
        
    def contains(self, item: str) -> bool:
        '''Returns if quantity of item > 0'''
        return self.inventory[item].item_count > 0

    def remove_item(self, item: str, quantity: int) -> None:
        '''Removes quantity of item to inventory'''
        self.inventory[item].item_count -= quantity
        if self.inventory[item].item_count < 0 and not self.inventory[item].negatives:
            self.inventory[item].item_count = 0
    
    def clear_item(self, item: str) -> None:
        '''Sets quantity of item to 0'''
        self.inventory[item].item_count = 0
        
    def get_all_items(self) -> list[str]:
        '''Returns list of all items with a count > 0'''
        items = []
        for item, item_data in self.inventory.items():
            if item_data.item_count > 0:
                items.append(item)
                
        return items
    
    def set_item_max(self, item: str, max: int) -> None:
        self.inventory[item].item_max = max
    
    def get_item_max(self, item: str) -> int:
        return self.inventory[item].item_max
    
    def set_item_negatives(self, item: str, negatives: bool) -> None:
        self.inventory[item].negatives = negatives
    
    def get_item_negatives(self, item: str) -> bool:
        return self.inventory[item].negatives
                