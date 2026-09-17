from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pydantic import BaseModel
import os


app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/posts")
async def return_posts():
    print(os.getenv("SQLITE_DB"))
    conn = sqlite3.connect(os.getenv("SQLITE_DB"))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS posts (" \
    "id INTEGER PRIMARY KEY AUTOINCREMENT," \
    "title TEXT NOT NULL," \
    "name TEXT NOT NULL," \
    "content TEXT NOT NULL," \
    "created_at DATETIME DEFAULT CURRENT_TIMESTAMP" \
    ");")
    cur.execute("SELECT id, title, name, content, created_at FROM posts;")
    rows = cur.fetchall()

    posts = [dict(row) for row in rows]
    conn.close()
    return posts

class Post(BaseModel):
    name: str
    title: str
    content: str

@app.post("/posts")
async def create_post(post: Post):
    conn = sqlite3.connect(os.getenv("SQLITE_DB"))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    print(post)
    cur.execute("CREATE TABLE IF NOT EXISTS posts (" \
    "id INTEGER PRIMARY KEY AUTOINCREMENT," \
    "title TEXT NOT NULL," \
    "name TEXT NOT NULL," \
    "content TEXT NOT NULL," \
    "created_at DATETIME DEFAULT CURRENT_TIMESTAMP" \
    ");")
    cur.execute(
        f"INSERT INTO posts (title, name, content) VALUES (?, ?, ?)",
        (post.title, post.name, post.content))
    conn.commit()
    conn.close()
    return post

@app.get("/health")
def get_health():
    return Response(status_code=200, content="Ok!")