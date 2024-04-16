from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from ..models.news_post import NewsPost
from ..models.news_post_details import NewsPostDetails


class NewsPostEntity(EntityBase):

    __tablename__ = "news_post"

    # need to be corrected
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    headline: Mapped[str] = mapped_column(String, nullable=False, default="")
    main_story: Mapped[str] = mapped_column(String, nullable=False, default="")
    author: Mapped[str] = mapped_column(String)
    organization_id: Mapped[int] = mapped_column(Integer, nullable=True)
    state: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String)
    image_url: Mapped[str] = mapped_column(String)
    time: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime] = mapped_column(DateTime)
    synopsis: Mapped[str] = mapped_column(String)

    @classmethod
    def from_model(cls, model: NewsPost) -> Self:
        return cls(
            id=model.id,
            headline=model.headline,
            slug=model.slug,
            main_story=model.main_story,
            author=model.author,
            organization_id=model.organization_id,
            state=model.state,
            image_url=model.image_url,
            time=model.time,
            modification_date=model.modification_date,
            synopsis=model.synopsis,
        )

    def to_model(self) -> NewsPost:
        return NewsPost(
            id=self.id,
            headline=self.headline,
            slug=self.slug,
            main_story=self.main_story,
            author=self.author,
            organization_id=self.organization_id,
            state=self.state,
            image_url=self.image_url,
            time=self.time,
            modification_date=self.modification_date,
            synopsis=self.synopsis,
        )

    def to_details_model(self) -> NewsPostDetails:
        return NewsPostDetails(
            id=self.id,
            headline=self.headline,
            slug=self.slug,
            main_story=self.main_story,
            author=self.author,
            organization_id=self.organization_id,
            state=self.state,
            image_url=self.image_url,
            time=self.time,
            modification_date=self.modification_date,
            synopsis=self.synopsis,
            ##events=None
        )
