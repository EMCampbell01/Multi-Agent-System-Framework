import multi_agent_system_framework as mas
import random


async def ant_process(self: mas.Agent, debug = True):
    
    if debug:
        print(f'ANT: {self.data.get("num")}')
    
    on_nest: bool = self.position == self.data['nest position']
    on_food: bool = len(self.environment.get_items_of_type_at_position(self.position, 'food')) > 0
    on_trail: bool = len(self.environment.get_items_of_type_at_position(self.position, 'trail')) > 0
    carrying_food: bool = self.inventory.contains('food')
    
    adjacent_positions: list[tuple[int, int]] = self.environment.get_adjacent_positions(self.position)
    adjacent_food_positions = []
    adjacent_trail_positions = []
    
    for adjacent_position in adjacent_positions:
        
        adjacent_food_items = self.environment.get_items_of_type_at_position(adjacent_position, 'food')
        adjacent_trail_items = self.environment.get_items_of_type_at_position(adjacent_position, 'trail')
        
        if len(adjacent_food_items) > 0:
            adjacent_food_positions.append(adjacent_position)
            
        if len(adjacent_trail_items) > 0:
            adjacent_trail_positions.append(adjacent_position)
            
    next_to_food: bool = len(adjacent_food_positions) > 0
    next_to_trail: bool = len(adjacent_trail_positions) > 0
    
    if on_food and not carrying_food:
        pick_up_food(self)
        
        if len(self.environment.get_items_of_type_at_position(self.position, 'food')) == 0:
            print(f'ANT: {self.data.get("num")} - clear trail = true')
            self.data['clear trail'] = True        
        
        elif len(adjacent_trail_positions) == 0:
            print(f'ANT: {self.data.get("num")} - leave trail = true')
            self.data['leave trail'] = True
      
    elif carrying_food:
        if on_nest:
            drop_food_in_nest(self)
            self.data['leave trail'] = False
            self.data['clear trail'] = False
        else:
            return_to_nest(self)
            
    elif on_trail:
        follow_trail_to_food(self, self.environment.get_items_of_type_at_position(self.position, 'trail')[0])
            
    elif next_to_food:
        print(f'ANT: {self.data.get("num")} - next to food, move to {adjacent_food_positions[0]}')
        move_to_position(self, adjacent_food_positions[0])
        
    elif next_to_trail:
        print(f'ANT: {self.data.get("num")} - next to trail, move to {adjacent_trail_positions[0]}')
        move_to_position(self, adjacent_trail_positions[0])
        
    else:
        print(f'ANT: {self.data.get("num")} - explore')
        explore(self)
    
def explore(self: mas.Agent):
    
    current_position = self.position
    adjacent_positions = self.environment.get_adjacent_positions(current_position)
    
    for position in adjacent_positions:
        
        if len(self.environment.get_items_of_type_at_position(position, 'food')) > 0:
            self.position = position
            return
            
    new_adjacent_positions = [position for position in adjacent_positions if position not in self.memory.get_partition_data('positions')]
    if new_adjacent_positions:
        new_position = random.choice(new_adjacent_positions)
    else:
        new_position = random.choice(adjacent_positions)
    
    self.position = new_position
    add_position_to_memory(self, self.position)

def pick_up_food(self: mas.Agent):
    print(f'ANT: {self.data.get("num")} - pick_up_food')
    food = self.environment.get_items_of_type_at_position(self.position, 'food')[0]
    food.inventory['food'] -= 1
    if food.inventory['food'] == 0:
        self.environment.delete_item(food.id)
        print(f'ANT: {self.data.get("num")} - deleted food')
    self.inventory.add_item('food', 1)

def return_to_nest(self: mas.Agent):
    
    nest_position = self.data.get('nest position')
    start_position = self.position
    
    move_x, move_y = 0, 0
    
    if start_position[0] < nest_position[0]:
        move_x = 1
    elif start_position[0] > nest_position[0]:
        move_x = -1            

    if start_position[1] < nest_position[1]:
        move_y = 1
    elif start_position[1] > nest_position[1]:
        move_y = -1
            
    new_position = (start_position[0] + move_x, start_position[1] + move_y)
    self.position = new_position
    
    if self.data['leave trail']:
        trail = mas.Item(
            item_type = 'trail',
            position = new_position,
            data = {'food direction': start_position}
        )
        self.environment.add_item(trail)
        print(f'ANT: {self.data.get("num")} - added trail {trail.position, trail.data["food direction"]}')
        
        
    if self.data.get('clear trail') == True:
        trails = self.environment.get_items_of_type_at_position(self.position, 'trail')
        for trail in trails:
            if trail.data.get('food direction') == start_position:
                print(f'ANT: {self.data.get("num")} - cleared trail {trail.position, trail.data["food direction"]}')
                self.environment.delete_item(trail.id)
                break
        
def drop_food_in_nest(self: mas.Agent):
    print(f'ANT: {self.data.get("num")} - drop_food_in_nest()')
    self.inventory.remove_item('food', 1)
    ant_nest = self.environment.get_items_of_type('ant nest')[0]
    ant_nest.data['food count'] += 1

def follow_trail_to_food(self: mas.Agent, trail: mas.Item):
    
    new_position = trail.data['food direction']
    food = self.environment.get_items_of_type_at_position(new_position, 'food')
    trails = self.environment.get_items_of_type_at_position(new_position, 'trail')
    
    if len(food) == 0 and len(trails) == 0:
        self.environment.delete_item(trail.id)
        explore(self)
    
    else:
        print(f'ANT: {self.data.get("num")} - follow trail to food self.position:{self.position}, trail:{trail.position, trail.data.get("food direction")}')
        self.position = new_position 
        
def add_position_to_memory(self: mas.Agent, position):
    self.memory.add_to_partition('positions', position)
    
def move_to_position(self: mas.Agent, position: tuple[int, int]):
    self.position = position