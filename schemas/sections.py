from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated

class SectionBase(BaseModel):
    name: Annotated[str, Field(..., min_length=5, max_length=80)]  # TODO: min and max length must be defined!!


class SectionCreate(SectionBase):
    pass


class SectionUpdate(SectionBase):
    pass


class Section(SectionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
