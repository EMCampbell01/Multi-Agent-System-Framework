from typing import TYPE_CHECKING, Union
from functools import wraps
from uuid import UUID
import asyncio
import uuid

if TYPE_CHECKING:
    from multi_agent_system_framework.item.item import Item
    from multi_agent_system_framework.agent.agent import Agent


class Environment():
    """
    The Environment class represents a two-dimensional space where agents and items can interact.
    It manages a collection of agents and items, validates their positions, and provides utilities
    to retrieve entities at specific locations. The environment also runs asynchronously, updating
    all agents by calling their respective `run` methods in each step of the simulation.
    
    Attributes:
        running (bool): Indicates whether the environment is actively running.
        id (UUID): A unique identifier for the environment instance.
        data (dict): A dictionary for storing custom data related to the environment.
        items (dict[UUID, Item]): A dictionary storing items in the environment, keyed by their UUIDs.
        agents (dict[UUID, Agent]): A dictionary storing agents in the environment, keyed by their UUIDs.
        size (tuple[int, int]): The dimensions (width, height) of the environment grid.
    """
    
    def __init__(self, size: tuple[int, int], data = {}):
        self.running = False
        self.id: UUID = uuid.uuid4()
        self.data: dict[str, any] = data
        self.items: dict[UUID, 'Item'] = {}
        self.agents: dict[UUID, 'Agent'] = {}
        self.size: tuple[int, int] = size
        
    @property
    def entities(self) -> dict[UUID, Union['Agent', 'Item']]:
        """Return a combined dictionary of agents and items."""
        entities = {**self.agents, **self.items}
        return entities
        
    async def run(self) -> None:
        """
        Run the environment's simulation asynchronously. This method continually updates
        all agents by calling their `run` method in parallel until the `running` attribute is set to False.
        Each agent operates concurrently using asyncio.gather.
        """
        self.running = True
        while self.running:
            await asyncio.gather(*(agent.run() for agent in self.agents.values()))

    # Position methods

    def is_valid_position(self, position: tuple[int, int]) -> bool:
        """Check if the position is within the bounds of the environment."""
        x, y = position
        max_x, max_y = self.size
        if 0 <= x < max_x and 0 <= y < max_y:
            return True
        else:
            return False

    def validate_position(func: callable) -> callable:
        """Decorator to validate if a given position is within environment bounds."""
        @wraps(func)
        def wrapper(self, position: tuple[int, int], *args, **kwargs):
            if self.is_valid_position(position):
                return func(self, position, *args, **kwargs)
            else:
                raise ValueError(f"Position {position} is out of bounds for environment size {self.size}.")
        return wrapper
    
    def get_adjacent_positions(self, position: tuple[int, int], diagonal=True) -> list[tuple[int, int]]:
        """Get a list of adjacent positions (including diagonals if specified) around a given position."""
        x, y = position
        adjacent_positions = []

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if diagonal:
            moves += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in moves:
            new_position = (x + dx, y + dy)
            if self.is_valid_position(new_position):
                adjacent_positions.append(new_position)

        return adjacent_positions
        
    # Agent methods  
           
    def add_agent(self, agent: 'Agent') -> None:
        """Add agent to enironment"""
        agent_id = agent.id
        self.agents[agent_id] = agent
        
    def get_agent(self, agent_id: UUID) -> 'Agent':
        """Get specified agent from environment"""
        return self.agents.get(agent_id)
                
    def delete_agent(self, agent_id: UUID) -> None:
        """Delete agent from environment"""
        del self.agents[agent_id]
    
    @validate_position  
    def get_agents_at_position(self, position: tuple[int, int]) -> list['Agent']:
        """Get a list of agents that are at the specified position."""
        return [agent for agent in self.agents.values() if agent.position == position]
    
    # Item methods
    
    def add_item(self, item: 'Item') -> None:
        """Add item to enironment"""
        item_id = item.id
        self.items[item_id] = item
        
    def get_item(self, item_id: UUID) -> 'Item':
        """Get specified item from environment"""
        return self.items.get(item_id)
                
    def delete_item(self, item_id: UUID) -> None:
        """Delete item from environment"""
        del self.items[item_id]
    
    @validate_position
    def get_items_at_position(self, position: tuple[int, int]) -> list['Item']:
        """Get a list of items that are at the specified position."""
        return [item for item in self.items.values() if item.position == position]
    
    def get_items_of_type(self, item_type: str) -> list['Item']:
        """Get a list of items that are of the specified type."""
        return [item for item in self.items.values() if item.item_type == item_type]
    
    @validate_position
    def get_items_of_type_at_position(self, position: tuple[int, int], item_type: str) -> list['Item']:
        """Get a list of items that are of the specified type and at the specified position."""
        return [item for item in self.items.values() if item.position == position and item.item_type == item_type]
        
    # Entity methods

    def get_entity(self, entity_id: UUID) -> Union['Agent', 'Item']:
        """Get an entity (agent or item) from the environment."""
        return self.entities.get(entity_id)
    
    @validate_position
    def get_entities_at_position(self, position: tuple[int, int]) -> list[Union['Agent', 'Item']]:
        """Get a list of agents and items that are at the specified position."""
        return [entity for entity in self.entities.values() if entity.position == position]
    