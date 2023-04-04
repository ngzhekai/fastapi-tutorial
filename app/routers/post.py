from fastapi import Depends, Response, status, HTTPException, APIRouter
from typing import List, Optional
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

# FastAPI路由函数 用来替代‘app’的FastAPI 在main.py里头
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cur.execute("SELECT * FROM posts")
    # posts = cur.fetchall()
    # print(
    #     f"the user id is '{current_user.id}' and email is '{current_user.email}'")
    # posts = db.query(models.Post).filter(models.Post.title.contains(
    #     search)).limit(limit).offset(skip).all()  # 返回所有用户的帖子
    # 假如 只要返回当前登入用户的帖子
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # 返回帖子 与 点赞数额
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(
            search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # 需要token 验证来执行一下的代码
    # cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #             (post.title, post.content, post.published))
    # new_post = cur.fetchone()
    # conn.commit()
    print(current_user.email)
    new_post = models.Post(
        **post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # 返回插入数据库的数据分配给变数new_post
    return new_post


@router.get("/latest", response_model=schemas.Post)
def get_latest_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = my_posts[len(my_posts)-1]
    post = db.query(models.Post).order_by(desc('id')).first()
    return post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cur.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found!")
    # 假如要限制当前登入用户只能查询自己的帖子
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # 删除帖子
    # cur.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cur.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist!")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #             (post.title, post.content, post.published, id))
    # updated_post = cur.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist!")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
