from fastapi import APIRouter, HTTPException
import crud.sections as sections
from exceptions import DbnotFoundException, SectionInUseError
from schemas.sections import Section, SectionCreate, SectionUpdate
from database import db

router = APIRouter(prefix="/sections", tags=["sections"])


@router.get("", response_model=list[Section])
def list_sections(db: db):
    return sections.list_sections(db)


@router.get("/{section_id}", response_model=Section)
def get_section(section_id: int, db: db):
    try:
        return sections.get_section(db, section_id)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Section {section_id} not found!!")


@router.post("", response_model=Section, status_code=201)
def create_section(section: SectionCreate, db: db):
    section = sections.create_section(db, section)
    db.commit()
    db.refresh(section)
    return section


@router.put("/{section_id}", response_model=Section)
def update_section(section_id: int, section: SectionUpdate, db: db):
    try:
        section = sections.update_section(db, section_id, section)
        db.commit()
        return section
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Section {section_id} not found!!")


@router.delete("/{section_id}", status_code=204)
def delete_section(section_id: int, db: db):
    try:
        sections.delete_section(db, section_id)
        db.commit()
    except SectionInUseError:
        raise HTTPException(
            status_code=400, detail="Cannot delete a section that has associated posts"
        )
