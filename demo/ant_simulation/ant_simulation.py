from .agent_process_methods.ant_feeder_processes import ant_feeder_process
from .utils.visualize_ant_simulation import visualize_ant_simulation
from .agent_process_methods.ant_processes import ant_process
import multi_agent_system_framework as mas
import asyncio

async def main():
    
    ENVIRONMENT_SIZE = (100,100)
    ANT_COUNT = 20
    ANT_SPEED = 0.01
    
    # Create environment
    
    environment = mas.Environment(ENVIRONMENT_SIZE)
          
    # Add ant nest item to environment 
    
    nest_position = (int(ENVIRONMENT_SIZE[0]/2), int(ENVIRONMENT_SIZE[1]/2))
    ant_nest = mas.Item(
        item_type='ant nest',
        position=(nest_position),
        data={'food count': 0}
    )
    environment.add_item(ant_nest)
    
    # Add ant agents to environment
    
    ant_agent_bp = mas.AgentBlueprint(
        agent_type = "Ant",
        environment = environment,
        process = ant_process,
        process_delay = ANT_SPEED,
        data={'leave trail': False, 'clear trail': False, 'nest position': nest_position}.copy(),
        position = nest_position,
    )
    
    ants = []
    for n in range(ANT_COUNT):
        ant = mas.Agent.create_agent(ant_agent_bp)
        ant.data['num'] = n
        ants.append(ant)    
    
    # Add ant feeder agent to environment
    
    ant_feeder_bp = mas.AgentBlueprint(
        agent_type = 'AntFeeder',
        process = ant_feeder_process,
        process_delay = 3,
        environment = environment,
        data = {},
    )
    ant_feeder = mas.Agent.create_agent(ant_feeder_bp)
    
    # Run environment
    
    await asyncio.gather(environment.run(), visualize_ant_simulation(environment))

if __name__ == "__main__":
    asyncio.run(main())
