import multi_agent_system_framework as mas
import asyncio
import random

async def ant_feeder_process(self: mas.Agent):
    
    environment_food_count = len(self.environment.state.get_entities_of_type('food'))
    if environment_food_count < 10:
        
        food = mas.Entity(
            entity_type='food',
            position=(random.randint(10,90),random.randint(10,90))
        )        
        
        self.environment.state.add_entity(food)
        print('food spawned')