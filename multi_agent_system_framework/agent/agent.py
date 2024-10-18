from multi_agent_system_framework.agent.sub_components.inventory import Inventory
from multi_agent_system_framework.agent.sub_components.memory import Memory
from multi_agent_system_framework.agent.sub_components.clock import Clock
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
import asyncio
import uuid

if TYPE_CHECKING:
    from multi_agent_system_framework.environment.environment import Environment


@dataclass
class AgentBlueprint():
    '''
    AgentBlueprint data class used to create agent child instances.
    
    Attributes:
        agent_type: str
        process: callable
        process_delay: float
        data: dict[str, any]
        position: tuple[int, int]
    '''
    
    agent_type: str
    environment: 'Environment' 
    process: callable
    process_delay: int = 1
    data: dict[str, any] = field(default_factory=dict)
    position: tuple[int | int] | None = None


class Agent(ABC):
    '''
    Abstract base class of all Agent objects. 
    
    Contains class method "create_agent" for creating instances of child agents.
    
    Agents represent an autonomous agents, which acts on the environment and items within it.
    '''
    
    def __init__(self, environment, process_delay = 1, data = {}, position = None) -> None:

        self.id = uuid.uuid4()
        self.running: bool = False
        self.process_delay: int = process_delay
        
        self.environment: 'Environment' = environment
        self.environment.add_agent(self)
         
        self.data: dict[str, any] = data
        self.position: tuple[int, int] = position
        
        self.inventory: Inventory = Inventory()
        self.memory: Memory = Memory()
        self.clock: Clock = Clock()
        
    @abstractmethod
    async def process(self) -> any:
        '''Place holder to be overwritten with intended behaviour logic in child class'''
        pass    
    
    async def run(self) -> None:
        '''
        The agent's main behavior loop 
        
        Calls the agent's process function every iteration and pauses for the specified delay between each iteration
        '''
        self.running = True
        while self.running:
            await self.process()
            await asyncio.sleep(self.process_delay)
            
    def stop_running(self) -> None:
        '''Disables agent'''
        self.running = False
        
    @classmethod
    def create_agent(cls, agent_blueprint: AgentBlueprint) -> 'Agent':
        '''Class method to create a custom child agent instance, based upon the data in a given agent blueprint'''
        
        class_name = f"{agent_blueprint.agent_type}Agent"
        environment = agent_blueprint.environment
        process = agent_blueprint.process
        process_delay = agent_blueprint.process_delay
        
        data = agent_blueprint.data.copy() if isinstance(agent_blueprint.data, dict) else agent_blueprint.data
        position = agent_blueprint.position

        CustomAgent = type(class_name, (Agent,), {
            'process': process
        })

        agent = CustomAgent(environment, process_delay, data, position)
        return agent
    
    def __del__(self) -> None:
        if self.environment:
            self.environment.delete_agent(self.id)
            
