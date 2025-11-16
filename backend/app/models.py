from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Post(BaseModel):
    text: str
    created_at: datetime
    id: str

class Signal(BaseModel):
    post: Post
    sentiment: str
    signal: str


