from collections import defaultdict

class AgentState():

    def __init__(self, directive:str='idle', attributes={}, inventory=None, memory=None, position=None) -> None:
        
        self.directive = directive
        self.attributes: dict[str, any] = attributes
        self.inventory: defaultdict[str, int] | None = defaultdict(int, inventory) if inventory is not None else None
        self.memory: dict[str, any] | None = memory
        self.position: tuple[int, int] | None = position 
        
        self.has_inventory: bool = inventory != None
        self.has_memory: bool = memory != None
        self.has_position: bool = position !=None
    
    def get_directive(self) -> str:
        return self.directive
    
    def set_directive(self, directive: str) -> None:
        self.directive = directive
    
    def get_attribute_value(self, attribute: str) -> any:
        return self.attributes.get(attribute)
    
    def set_attribute_value(self, attribute: str, value: any) -> None:
        self.attributes[attribute] = value
        
    def get_inventory_item_count(self, item: str) -> int:
        return self.inventory.get(item)
    
    def set_inventory_item_count(self, item: str, count: int) -> None:
        self.inventory[item] = count
        
    def add_to_inventory(self, item: str, count: int) -> None:
        self.inventory[item] += count
        
    def subtract_from_inventory(self, item: str, count: int) -> None:
        self.inventory[item] -= count
        
    def get_position(self) -> tuple[int, int] | None:
        return self.position
    
    def set_position(self, position: tuple[int, int]) -> None:
        self.position = position