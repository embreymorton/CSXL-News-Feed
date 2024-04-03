from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self

from ..models.news_post import NewsPost

class NewsPostEntity(EntityBase):

    __tablename__ = "news_post"

    #need to be corrected
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    headline: Mapped[str] = mapped_column(String, nullable=False, default="")
    main_story: Mapped[str] = mapped_column(String, nullable=False, default="")
    author: Mapped[str] = mapped_column(String)
    organization: Mapped[str] = mapped_column(String)
    state: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String)
    image_url: Mapped[str] = mapped_column(String)
    publish_date: Mapped[str] = mapped_column(String)
    modification_date: Mapped[str] = mapped_column(String)


    @classmethod
    def from_model(cls, model: NewsPost) -> Self:
        return None
    

    def to_model(self) -> NewsPost:
        return None
    
