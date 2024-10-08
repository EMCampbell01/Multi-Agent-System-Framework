from dataclasses import dataclass
from typing import Callable
from .agent import Agent
from .agent_environment import AgentEnvironment

@dataclass
class AgentBlueprint():

    agent_type: str
    process: Callable
    sleep_timer: int
    environment: AgentEnvironment 
    attributes: dict[str, any]
    memory: dict[str, any] | None = None
    inventory: dict[str, int] | None = None
    position: tuple[int | int] | None = None