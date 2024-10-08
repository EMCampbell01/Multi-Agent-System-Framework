from .agent import Agent
from .agent_blueprint import AgentBlueprint
from .agent_environment import AgentEnvironment
from.state_components.agent_state import AgentState

def create_agent(agent_blueprint: AgentBlueprint, environment: AgentEnvironment) -> Agent:
    
    class_name = f"{agent_blueprint.agent_type}Agent"

    CustomAgent = type(class_name, (Agent,), {
        'process': agent_blueprint.process
    })

    agent_state = AgentState(
        attributes=agent_blueprint.attributes, 
        inventory=agent_blueprint.inventory,
        position=agent_blueprint.position,
        memory=agent_blueprint.memory
    )

    agent = CustomAgent(environment, agent_state, agent_blueprint.sleep_timer)
    return agent
    
    