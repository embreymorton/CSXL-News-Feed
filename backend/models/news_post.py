from pydantic import BaseModel
from user import User
from organization import Organization

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
    author: User
    organization: Organization | None = None
    state: str
    slug: str
    image_url: str 
    publish_date: str
    modification_date: str

