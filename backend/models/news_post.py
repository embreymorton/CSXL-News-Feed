from datetime import datetime
from pydantic import BaseModel

# from backend.test.services.news_post.news_post_demo_data import date_maker


# from test.services.news_post.news_post_demo_data import date_maker

__authors__ = ["Embrey Morton", "Ishmael Percy", "Jayson Mbugua", "Alphonzo Dixon"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class NewsPost(BaseModel):
    """
    Pydantic model to represent a `NewsPost`.

    This model is based on the `NewsPostEntity` model, which defines the shape
    of the `NewsPost` database in the PostgreSQL database.
    """

    id: int | None = None
    headline: str
    main_story: str
    author_id: int 
    organization_id: int | None = None
    state: str
    slug: str
    image_url: str | None = None
    time: datetime
    modification_date: datetime
    synopsis: str | None = None