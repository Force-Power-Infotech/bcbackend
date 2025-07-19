from typing import List, Optional
from enum import Enum
from pydantic import BaseModel

class ItemType(str, Enum):
    drill = "drill"
    drill_group = "drill_group"

class SearchResult(BaseModel):
    id: int
    name: str
    type: ItemType
    description: Optional[str] = None
    # Fields specific to drills
    drill_type: Optional[str] = None
    # Fields specific to drill groups
    tags: Optional[List[str]] = None
    difficulty: Optional[int] = None

class SearchResponse(BaseModel):
    total: int
    items: List[SearchResult]
