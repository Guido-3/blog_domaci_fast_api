from fastapi import APIRouter, HTTPException
from database import db
from crud import tags
router = APIRouter(prefix="/tags", tags=["tags"])

@router.get("", response_model=list[dict])
def all_tags_with_posts_count(db: db): # type: ignore
    return tags.all_tags_with_posts_count(db=db)