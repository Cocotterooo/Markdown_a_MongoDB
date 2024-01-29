from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4


@dataclass
class Author:
    "Dataclass for a Post Author"
    name: str


@dataclass
class Post:
    "Dataclass for a Post"
    title: str
    content: str
    author: Author
    title_nonce: str = ""
    created_at: datetime = None
    updated_at: datetime = None
    view: int = 0
    likes: int = 0
    dislikes: int = 0

    def __post_init__(self):
        # TODO: title part of title_nonce needs urlification
        self.title_nonce = f"{self.title}-{str(uuid4())}"
        self.created_at = datetime.now()
        self.updated_at = self.created_at
