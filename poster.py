from dataclasses import asdict
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from posts import Post

class DAIPoster:
    client: MongoClient | None = None

    def __init__(
            self,
            user: str | None = None,
            host: str | None = None,
            name: str | None = None,
            password: str | None = None,
            to_local_db: bool = True
        ):
        self.user = user
        self.host = host
        self.name = name
        self.password = password
        self.to_local_db = to_local_db

    def connect(self) -> bool:
        """Connects to either a local or a remote MondoDB client

        The database client is pinged to check its connection
        """

        if self.to_local_db:
            client = MongoClient("mongodb://localhost")
        else:
            client = MongoClient(
                f"mongodb+srv://{self.user}:{self.password}@{self.host}/{self.name}"
                "?retryWrites=true&w=majority"
            )
        try:
            client.admin.command("ping")
        except ConnectionFailure:
            return False

        self.client = client
        return True

    def post(self, posts: list[Post]):
        """Uploads `posts` to the database."""
        if not self.connect():
            return None

        return (
            self.client
            .get_database(self.name)
            .get_collection("posts")
            .insert_many([asdict(post) for post in posts])
        )

    def find_by_title(self, title: str):
        return self.client.self.name.posts.find_one({"title": title})
