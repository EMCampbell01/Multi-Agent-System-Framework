from dataclasses import dataclass, field
from uuid import uuid4, UUID

@dataclass
class Entity:
    entity_type: str
    position: tuple[int, int] | None
    data: dict[str, any] | None = None
    id: UUID = field(default_factory=uuid4)
    
