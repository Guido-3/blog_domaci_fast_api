from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, select
from crud.sections import get_section
from crud.tags import get_or_create_tags
from exceptions import DbnotFoundException
from models.posts import Post
from models.tags import Tag
from schemas.posts import FilterPosts, PostCreate, PostUpdateFull, PostUpdatePartial

def delete_tags_after_deleting_post(db: Session, tags_to_check: list[Tag]):
        for tag in tags_to_check:
            tag_count = db.execute(select(Post).where(Post.tags.contains(tag))).scalar_one_or_none()
            
            if tag_count == 0:
                db.delete(tag)

def delete_tags_after_update(db: Session, tags_to_check: list[Tag], new_tags: list[Tag]):
    for tag in tags_to_check:
        if tag not in new_tags:
            tag_count = db.execute(select(Post).where(Post.tags.contains(tag))).scalar_one_or_none()
            
            if tag_count == 0:
                db.delete(tag)

def get_post(db: Session, post_id: int) -> Post:
    post = db.get(Post, post_id)
    if not post:
        raise DbnotFoundException
    return post


def list_posts(db: Session, filters: Optional[FilterPosts] = None) -> list[Post]:
    query = select(Post)

    if filters:
        if filters.title:
            query = query.where(Post.title.ilike(f"%{filters.title}%"))

        if filters.section_id is not None:
            query = query.where(Post.section_id == filters.section_id)

        if filters.tags:
            query = query.join(Post.tags).where(and_(*[Tag.name == tag for tag in filters.tags]))

        if filters.created_at_gt:
            query = query.where(Post.created_at >= filters.created_at_gt)

        if filters.created_at_lt:
            query = query.where(Post.updated_at <= filters.created_at_lt)

    return db.scalars(query).all()


def create_post(db: Session, post_data: PostCreate) -> Post:
    section = get_section(db, post_data.section_id)

    new_post = Post(**post_data.model_dump(exclude={"tags"}))
    new_post.section = section

    if post_data.tags:
        tags = get_or_create_tags(db, post_data.tags)
        new_post.tags = tags

    db.add(new_post)
    return new_post

def update_post_full(db: Session, post_id: int, post_data: PostUpdateFull) -> tuple[Post, list[Tag], list[Tag]]:
    post_being_updated = get_post(db, post_id)
    tags_to_check = post_being_updated.tags.copy()

    update_data = post_data.model_dump(exclude={"tags"})

    for key, value in update_data.items():
        setattr(post_being_updated, key, value)

    new_tags = get_or_create_tags(db, post_data.tags)
    post_being_updated.tags = new_tags

    return post_being_updated, tags_to_check, new_tags  

def update_post_partial(db: Session, post_id: int, post_data: PostUpdatePartial) -> tuple[Post, list[Tag], list[Tag]]:
    post_being_updated = get_post(db, post_id)
    tags_to_check = post_being_updated.tags.copy()

    update_data = post_data.model_dump(exclude_unset=True, exclude={"tags"})

    for key, value in update_data.items():
        setattr(post_being_updated, key, value)

    if post_data.tags:
        new_tags = get_or_create_tags(db, post_data.tags)
        post_being_updated.tags = new_tags
    else:
        new_tags = tags_to_check

    return post_being_updated, tags_to_check, new_tags


def delete_post(db: Session, post_id: int) -> list[Tag]:

    post = get_post(db, post_id)
    tags_to_check = post.tags.copy()
    
    db.delete(post)
    
    return tags_to_check