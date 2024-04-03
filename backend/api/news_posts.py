"""News Post API

News Post routes are used to create, retrieve, update, and delete News Posts."""

from fastapi import APIRouter, Depends

from ..models.news_post import NewsPost

from ..services.news_post import NewsPostService

from ..api.authentication import registered_user
from ..models.user import User

api = APIRouter(prefix="/api/news_posts")
openapi_tags = {
    "name": "Posts",
    "description": "Create, update, delete, and retrieve News Posts.",
}


@api.get("", response_model=list[NewsPost], tags=["Posts"])
def get_posts(news_service: NewsPostService = Depends()) -> list[NewsPost]:

    return news_service.all()


@api.post("", response_model=NewsPost, tags=["Posts"])
def create_post(
    post: NewsPost,
    subject: User = Depends(registered_user),
    news_service: NewsPostService = Depends(),
) -> NewsPost:

    return news_service.create(subject, post)


@api.put("", response_model=NewsPost, tags=["Posts"])
def update_post(
    post: NewsPost,
    subject: User = Depends(registered_user),
    news_service: NewsPostService = Depends(),
) -> NewsPost:

    return news_service.update(subject, post)


@api.delete("", tags=["Posts"])
def delete_post(
    slug: str,
    subject: User = Depends(registered_user),
    news_service: NewsPostService = Depends(),
) -> None:

    return news_service.delete(subject, id)
