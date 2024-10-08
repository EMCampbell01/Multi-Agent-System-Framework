from uuid import UUID

class EnvironmentState():

    def __init__(self, attributes={}, grid_map_size: tuple[int, int] = (100,100)) -> None:
        
        self.attributes: dict[str, any] = attributes
        self.grid_map_size = grid_map_size
        self.grid_map: list[list[any]] = [[[] for _ in range(grid_map_size[0])] for _ in range(grid_map_size[1])]
        self.entities: dict[UUID, any] = {}
        
    def get_attribute_value(self, attribute: str) -> any:
        return self.attributes.get(attribute)
    
    def set_attribute_value(self, attribute: str, value: any) -> None:
        self.attributes[attribute] = value
    
    def get_entity(self, entity_id: UUID) -> any:
        return self.entities.get(entity_id)
    
    def get_entities_of_type(self, entity_type: str) -> list[any]:
        entities = []
        for entity in self.entities.values():
            if entity.entity_type == entity_type:
                entities.append(entity)
        return entities
    
    def get_entities_at_position(self, position: tuple[int, int]) -> list[any]:
        entities = []
        x, y = position
        for entity_id in self.grid_map[x][y]:
            entities.append(self.entities[entity_id])
        return entities
        
    def add_entity(self, entity) -> None:
        self.entities[entity.id] = entity
        
        if entity.position:
            x, y = entity.position
            self.grid_map[x][y].append(entity.id)
    
    def remove_entity(entity_id) -> None:
        pass
    
    def remove_entity_type(entity_type: str) -> None:
        pass
    
    def get_adjacent_positions(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        
        x, y = position
        max_x, max_y = self.grid_map_size
        
        adjacent_coords = [
            [x + dx, y + dy]
            for dx in (-1, 0, 1) 
            for dy in (-1, 0, 1) 
            if not (dx == 0 and dy == 0)
            and 0 <= x + dx < max_x
            and 0 <= y + dy < max_y
        ]
        
        return adjacent_coords
    
    
    