from sqlalchemy import select, func
from models.tags import Tag
from sqlalchemy.orm import Session
from models.posts import Post

def get_or_create_tags(db: Session, tag_names: list[str]) -> list[Tag]:
    unique_tag_names = list(set(tag_names))

    # Step 1: Retrieve existing Tags from the db
    existing_tags_query = select(Tag).where(Tag.name.in_(unique_tag_names))
    existing_tags = db.scalars(existing_tags_query).all()

    existing_tag_names = {tag.name for tag in existing_tags}

    # Step 2:  identifiy tag names to be created
    new_tag_names = set(unique_tag_names) - existing_tag_names
    new_tags = [Tag(name=name) for name in new_tag_names]  # list comprehension

    # new_tags = []
    # for name in new_tag_names:
    #     tag = Tag(name=name)
    #     new_tags.apend(tag)

    db.add_all(new_tags)
    return existing_tags + new_tags

def all_tags_with_posts_count(db: Session) -> list[dict]:
    tags_query = (
        select(
        Tag.id,
        Tag.name,
        func.count(Post.id).label("posts_count")
        ).join(Tag.posts)
        .group_by(Tag.id, Tag.name)
    )

    result = db.execute(tags_query).all()

    tags = [
        {"id": tag_id, "name": tag_name, "posts_count": posts_count}
        for tag_id, tag_name, posts_count in result
    ]

    return tags