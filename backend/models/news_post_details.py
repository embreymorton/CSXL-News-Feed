from pydantic import BaseModel

from backend.models.organization import Organization
from backend.models.user import User
from .news_post import NewsPost

__authors__ = ["Embrey Morton", "Ishmael Percy", "Jayson Mbugua", "Alphonzo Dixon"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class NewsPostDetails(NewsPost):

    author: User | None = None
    organization: Organization | None = None
