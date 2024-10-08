from .utils.ant_processes import ant_process
from .utils.ant_feeder_processes import ant_feeder_process
from .utils.visualize_ant_simulation import visualize_ant_simulation
import multi_agent_system_framework as mas
import asyncio

async def main():
    
    # Create environment
    environment = mas.AgentEnvironment()
          
    # Add ant nest entity to environment 
    nest = mas.Entity(
        entity_type='nest',
        position=(50,50)
    )
    environment.state.add_entity(nest)

    # Add ant agents to environment
    ant_agent_bp = mas.AgentBlueprint(
        agent_type="Ant",
        process=ant_process,
        sleep_timer=0.1,
        environment=environment,
        attributes={'leave trail':False, 'nest position': (50,50)},
        memory={'positions': []},
        inventory={'food':0},
        position= (50,50),
    )
    ants = []
    for _ in range(10):
        ant = mas.create_agent(ant_agent_bp, environment)
        ants.append(ant)    
    
    # Add ant feeder agent to environment
    ant_feeder_bp = mas.AgentBlueprint(
        agent_type='AntFeeder',
        process=ant_feeder_process,
        sleep_timer=15,
        environment=environment,
        attributes={},
    )
    ant_feeder = mas.create_agent(ant_feeder_bp, environment)
    
    # Run environment
    await asyncio.gather(environment.run(), visualize_ant_simulation(environment, ants))

if __name__ == "__main__":
    asyncio.run(main())
