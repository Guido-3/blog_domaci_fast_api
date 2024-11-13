from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
import crud.posts as posts
from exceptions import DbnotFoundException
from schemas.posts import FilterPosts, Post, PostCreate, PostUpdatePartial, PostUpdateFull
from database import db

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=list[Post])
def list_posts(db: db, filters: Annotated[FilterPosts, Query()]): 
    return posts.list_posts(db, filters)


@router.get("/{post_id}", response_model=Post)
def get_post(post_id: int, db: db):
    try:
        return posts.get_post(db, post_id)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found!")


@router.post("", response_model=Post, status_code=201)
def create_post(post: PostCreate, db: db):
    post = posts.create_post(db, post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/{post_id}", response_model=Post)
def update_post_full(post_id: int, post: PostUpdateFull, db: db):
    try:
        post = posts.update_post_full(db, post_id, post)
        db.commit()
        db.refresh(post)
        return post
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found!")


@router.patch("/{post_id}", response_model=Post)
def update_post_partial(post_id: int, post: PostUpdatePartial, db: db):
    try:
        post = posts.update_post_partial(db, post_id, post)
        db.commit()
        db.refresh(post)
        return post
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found!")


@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: db):
    try:
        posts.delete_post(db, post_id)
        db.commit()
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found!")
