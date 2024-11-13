from sqlalchemy import select
from sqlalchemy.orm import Session
from exceptions import DbnotFoundException, SectionInUseError
from models.posts import Post
from models.sections import Section
from models.tags import Tag
from schemas.sections import SectionCreate, SectionUpdate


def get_section(db: Session, section_id: int) -> Section:
    section = db.get(Section, section_id)
    if not section:
        raise DbnotFoundException
    return section


def list_sections(db: Session) -> list[Section]:
    return db.scalars(select(Section)).all()


def create_section(db: Session, section_data: SectionCreate) -> Section:
    new_section = Section(**section_data.model_dump())
    db.add(new_section)
    return new_section


def update_section(
    db: Session, section_id: int, section_data: SectionUpdate
) -> Section:
    section_being_updated = get_section(db, section_id)
    update_data = section_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(section_being_updated, key, value)

    return section_being_updated


def delete_section(db: Session, section_id: int) -> None:
    # Check if there is any Post associated with this Section
    query = select(Post).where(Post.section_id == section_id)
    post = db.scalar(query)

    if post:
        raise SectionInUseError

    section = get_section(db, section_id)
    db.delete(section)
