"""News Post API

News Post routes are used to create, retrieve, update, and delete News Posts."""

from fastapi import APIRouter, Depends

from backend.models.news_post_details import NewsPostDetails
from backend.models.pagination import EventPaginationParams, Paginated
from backend.services.organization import OrganizationService
from backend.services.user import UserService

from ..models.news_post import NewsPost

from ..services.news_post import NewsPostService

from ..api.authentication import registered_user
from ..models.user import User

api = APIRouter(prefix="/api/news")
openapi_tags = {
    "name": "News",
    "description": "Create, update, delete, and retrieve News Posts.",
}


@api.get("", response_model=list[NewsPostDetails], tags=["News"])
def get_all_posts(news_service: NewsPostService = Depends(),
                  subject: User = Depends(registered_user)) -> list[NewsPostDetails]:

    return news_service.all(subject)

@api.get("/organization/{slug}", responses={404: {"model": None}}, response_model=list[NewsPostDetails], tags=["News"])
def get_posts_by_organization(
    slug: str,
    subject: User = Depends(registered_user),
    news_service: NewsPostService = Depends(),
    organization_service: OrganizationService = Depends(),
) -> list[NewsPostDetails]:
    """
    Get all posts from an organization

    Args:
        slug: a valid str representing a unique Organization
        subject: a valid User model representing the currently logged in User
        news_service: a valid NewsPostService
        organization_service: a valid OrganizationService

    Returns:
        list[NewsPostDetails]: All `NewsPostDetails`s in the `NewsPost` database table from a specific organization
    """
    organization = organization_service.get_by_slug(slug)
    return news_service.get_posts_by_organization(organization, subject)

@api.get("/author/{id}", responses={404: {"model": None}}, response_model=list[NewsPostDetails], tags=["News"])
def get_posts_by_author(
    id: int,
    subject: User = Depends(registered_user),
    news_service: NewsPostService = Depends(),
    user_service: UserService = Depends(),
) -> list[NewsPostDetails]:
    """
    Get all posts from a user

    Args:
        id: a valid int representing a unique Organization
        subject: a valid User model representing the currently logged in User
        news_service: a valid NewsPostService
        user_service: a valid UserService

    Returns:
        list[NewsPostDetails]: All `NewsPostDetails`s in the `NewsPost` database table from a specific user
    """
    author = user_service.get_by_id(id)
    return news_service.get_posts_by_user(author, subject)

@api.get("/author/drafts/{id}", responses={404: {"model": None}}, response_model=list[NewsPostDetails], tags=["News"])
def get_drafts_by_author(
    id: int,
    subject: User = Depends(registered_user),
    news_service: NewsPostService = Depends(),
    user_service: UserService = Depends(),
) -> list[NewsPostDetails]:
    """
    Get all drafts from a user

    Args:
        id: a valid int representing a unique Organization
        subject: a valid User model representing the currently logged in User
        news_service: a valid NewsPostService
        user_service: a valid UserService

    Returns:
        list[NewsPostDetails]: All `NewsPostDetails` drafts in the `NewsPost` database table from a specific user
    """
    author = user_service.get_by_id(id)
    return news_service.get_drafts_by_user(author, subject)


@api.get("/paginate", tags=["News"])
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

@api.get("/paginate/unauthenticated", tags=["News"])
def list_posts_unauthenticated(
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
    return news_service.get_paginated_posts(pagination_params)


@api.get("/published", response_model=list[NewsPostDetails], tags=["News"])
def get_published_posts(news_service: NewsPostService = Depends()) -> list[NewsPostDetails]:

    return news_service.get_published()


@api.get("/incoming", response_model=list[NewsPostDetails], tags=["News"])
def get_incoming_posts(news_service: NewsPostService = Depends(),
              subject: User = Depends(registered_user)) -> list[NewsPostDetails]:

    return news_service.get_incoming(subject)


@api.get("/archived", response_model=list[NewsPostDetails], tags=["News"])
def get_archived_posts(news_service: NewsPostService = Depends(),
              subject: User = Depends(registered_user)
              ) -> list[NewsPostDetails]:

    return news_service.get_archived(subject)

@api.get("/drafts", response_model=list[NewsPostDetails], tags=["News"])
def get_drafts(news_service: NewsPostService = Depends(),
              subject: User = Depends(registered_user)) -> list[NewsPostDetails]:

    return news_service.get_drafts(subject)

@api.get(
    "/{slug}",
    responses={404: {"model": None}},
    response_model=NewsPostDetails,
    tags=["News"],
)
def get_post_by_slug(slug: str, news_service: NewsPostService = Depends()) -> NewsPostDetails:
    return news_service.get_by_slug(slug)


@api.post("", response_model=NewsPostDetails, tags=["News"])
def create_post(
    post: NewsPost,
    subject: User = Depends(registered_user),
    news_service: NewsPostService = Depends(),
) -> NewsPostDetails:

    return news_service.create(subject, post)


@api.put("", responses={404: {"model": None}}, response_model=NewsPostDetails, tags=["News"])
def update_post(
    post: NewsPost,
    subject: User = Depends(registered_user),
    news_service: NewsPostService = Depends(),
) -> NewsPostDetails:

    return news_service.update(subject, post)


@api.delete("/{slug}", responses={404: {"model": None}}, response_model=None, tags=["News"])
def delete_post(
    slug: str,
    subject: User = Depends(registered_user),
    news_service: NewsPostService = Depends(),
):
    
    news_service.delete(subject, slug)
