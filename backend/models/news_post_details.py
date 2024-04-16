from pydantic import BaseModel
from .event import Event
from .news_post import NewsPost

__authors__ = ["Embrey Morton", "Ishmael Percy", "Jayson Mbugua", "Alphonzo Dixon"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class NewsPostDetails(NewsPost):

    events: list[Event] | None = None
