import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, insert_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, onupdate=func.now(), nullable=True
    )
    section_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sections.id"), nullable=False
    )

    section: Mapped["Section"] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(
        secondary="post_tags", back_populates="posts"
    )
