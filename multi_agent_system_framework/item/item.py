from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Item:
    '''
    Items represent basic entities that exist within an environment. 
    They may store state, but do not have their own behaviour. They are acted upon by agents
    '''
    item_type: str
    position: tuple[int, int] | None
    data: dict[str, any] | None = None
    inventory: dict[str, int] | None = None
    id: UUID = field(default_factory=uuid4)