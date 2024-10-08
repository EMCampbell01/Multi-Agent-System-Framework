from multi_agent_system_framework.state_components.environment_state import EnvironmentState
from multi_agent_system_framework.agent import Agent
from typing import Dict
from uuid import UUID
import asyncio

class AgentEnvironment():
    
    instance = None
    
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(AgentEnvironment, cls).__new__(cls)
            cls.instance._state = EnvironmentState()
            cls.instance._agents = {}
            cls.instance._running = False
            
        return cls.instance
    
    @property
    def state(self) -> EnvironmentState:
        return self._state
    
    @property
    def agents(self) -> dict[UUID, Agent]:
        return self._agents
    
    def add_agent(self, agent: any) -> None:
        """Add agent to enironment"""
        agent_id = agent.get_id()
        self.agents[agent_id] = agent
        
    def get_agent(self, agent_id: UUID):
        """Get specified agent from environment"""
        return self.agents.get(agent_id)
        
    def get_agents(self) -> Dict[UUID, any]:
        """Get agent dict for environment"""
        return self.agents
        
    def delete_agent(self, agent_id: UUID) -> None:
        """Delete agent from environment"""
        del self.agents[agent_id]
        
    async def run(self) -> None:
        self.running = True
        while self.running:
            await asyncio.gather(*(agent.run() for agent in self.agents.values()))
