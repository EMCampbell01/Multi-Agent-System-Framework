import multi_agent_system_framework as mas
import asyncio
import random

async def ant_feeder_process(self: mas.Agent):
    
    environment_food_count = len(self.environment.get_items_of_type('food'))
    if environment_food_count < 10:
        
        environment_size = self.environment.size
        
        food = mas.Item(
            item_type = 'food',
            position = (random.randint(0, environment_size[1]), random.randint(0, environment_size[1])),
            inventory = {'food': random.randint(1, 20)}
        )        
        self.environment.add_item(food)