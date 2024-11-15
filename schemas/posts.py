from datetime import datetime
from typing import Annotated, Optional, Union
from pydantic import BaseModel, ConfigDict, Field

from schemas.sections import Section
from schemas.tags import Tag


class PostBase(BaseModel):
    title: Annotated[str, Field(..., max_length=60, min_length=6)]
    body: str
    tags: list[str] = []


class PostCreate(PostBase):
    section_id: int


class PostUpdateFull(PostBase):
    title: Annotated[str, Field(max_length=60)]
    body: Annotated[str, Field(min_length=50)]
    section_id: int
    tags: list[str]


class PostUpdatePartial(PostBase):
    title: Annotated[Optional[str], Field(max_length=60)] = None
    body: Annotated[Optional[str], Field(min_length=50)] = None
    section_id: Optional[int] = None
    tags: Optional[list[str]] = None


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: Union[datetime, None] = None
    section: Section
    tags: list[Tag] = []

    model_config = ConfigDict(from_attributes=True)


class FilterPosts(BaseModel):
    title: Optional[str] = None
    section_id: Optional[int] = None
    tags: Optional[list[str]] = None
    created_at_gt: Optional[datetime] = None
    created_at_lt: Optional[datetime] = None
    