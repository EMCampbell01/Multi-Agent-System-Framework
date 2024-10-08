import multi_agent_system_framework as mas
import random

async def ant_process(self: mas.Agent):
    
    directive = self.state.get_directive()
    
    if directive == 'explore':
        explore(self)
    else:
        return_to_nest(self)

def explore(self: mas.Agent):
    
    current_position = self.state.get_position()
    entities = self.environment.state.get_entities_at_position(current_position)
    
    on_trail = False
    for entity in entities:
        if entity.entity_type == 'food trail':
            print('on food trail!!!')
            new_position = entity.data['end']
            on_trail = True
            break
    
    if not on_trail:
        adjacent_positions = self.environment.state.get_adjacent_positions(current_position)
        new_adjacent_positions = [position for position in adjacent_positions if position not in self.state.memory['positions']]
        
        if new_adjacent_positions:
            new_position = random.choice(new_adjacent_positions)
        else:
            new_position = random.choice(adjacent_positions)
    
    self.state.set_position(new_position)
    self.state.memory['positions'].append(new_position)
    
    entities = self.environment.state.get_entities_at_position(new_position)
    for entity in entities:
        if entity.entity_type == 'food':
            print('on food!!!')
            self.state.set_directive('return to nest')
            self.state.set_attribute_value('leave trail', True)
        
def return_to_nest(self: mas.Agent):
    
    nest_position = self.state.get_attribute_value('nest position')
    start_position = self.state.get_position()
    
    if start_position[0] < nest_position[0]:
        move_x = 1
    elif start_position[0] > nest_position[0]:
        move_x = -1
    else:
        move_x = 0

    if start_position[1] < nest_position[1]:
        move_y = 1
    elif start_position[1] > nest_position[1]:
        move_y = -1
    else:
        move_y = 0
        
    new_position = (start_position[0] + move_x, start_position[1] + move_y)
    self.state.set_position(new_position)
    
    if new_position == nest_position:
        self.state.set_directive('explore')
        self.state.set_attribute_value('leave trail', False)
        
    if self.state.get_attribute_value('leave trail'):
        trail = mas.Entity(
            entity_type='food trail',
            position=new_position,
            data={'end': start_position}
        )
        
        self.environment.state.add_entity(trail)