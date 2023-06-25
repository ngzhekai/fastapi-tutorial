from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


print(settings.database_password)
# 可以移除一下代码 毕竟使用alembic 迁移数据库 就没必要了
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# origins是指我们创造的API 能在什么网址上使用fetch
# 这CORSMiddleware功能是用来确保 前端 与 后端 是跑着相同的网址与网口
origins = [
    "https://www.google.com",
    "https://fastapi.tiangolo.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Welcome to my social media backend API! \
            This is hosted on Render PaaS Platform, give it a '/docs' on the URL\
            to redirect to the Swagger UI"}
