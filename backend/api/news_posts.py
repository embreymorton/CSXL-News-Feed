"""News Post API

News Post routes are used to create, retrieve, update, and delete News Posts."""

from fastapi import APIRouter, Depends

from backend.models.news_post_details import NewsPostDetails
from backend.models.pagination import EventPaginationParams, Paginated

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

@api.get("/paginate", tags=["Posts"])
def list_posts(
    subject: User = Depends(registered_user),
    news_service: NewsPostService = Depends(),
    order_by: str = "time",
    ascending: str = "true",
    filter: str = "",
    range_start: str = "",
    range_end: str = "",
) -> Paginated[NewsPostDetails]:
    """List posts in time range via standard backend pagination query parameters."""

    pagination_params = EventPaginationParams(
        order_by=order_by,
        ascending=ascending,
        filter=filter,
        range_start=range_start,
        range_end=range_end,
    )
    return news_service.get_paginated_posts(pagination_params, subject)

@api.get(
    "/{slug}",
    responses={404: {"model": None}},
    response_model=NewsPost,
    tags=["Posts"],
)
def get_post_by_slug(
    slug: str, news_service: NewsPostService = Depends()
) -> NewsPost:
    return news_service.get_by_slug(slug)

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

    return news_service.delete(subject, slug)
