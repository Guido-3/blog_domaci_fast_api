from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated

class TagBase(BaseModel):
    name: Annotated[str, Field(..., min_length=2, max_length=15)]  # TODO: min and max length must be defined!!


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
