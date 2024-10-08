from .state_components.agent_state import AgentState
import asyncio
import uuid

class Agent():
    
    def __init__(self, environment, state, sleep_time=1) -> None:
        
        self.id = uuid.uuid4()
        self.running = False
        
        self.environment = environment
        self.environment.add_agent(self)
        
        self.state: AgentState = state
        
        self.sleep_time = sleep_time
    
    async def run(self) -> any:
        
        self.running = True
        while self.running:
            await self.process()
            await asyncio.sleep(self.sleep_time)
            
    def stop_running(self) -> None:
        self.running = False
    
    async def process(self) -> any:
        pass
    
    def get_id(self) -> uuid.UUID:
        return self.id
    
    def get_sleep_time(self) -> int:
        return self.sleep_time
    
    def set_sleep_time(self, sleep_time: int) -> None:
        self.sleep_time = sleep_time
    
    def __del__(self) -> None:
        if self.environment:
            self.environment.remove_agent(self.get_id())