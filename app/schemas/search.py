from typing import List, Optional
from pydantic import BaseModel

class SearchResult(BaseModel):
    id: int
    name: str
    type: str  # "drill" or "drill_group"
    description: Optional[str] = None

class SearchResponse(BaseModel):
    items: List[SearchResult]
    total: int
