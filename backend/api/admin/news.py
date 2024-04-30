"""News administration API."""

from fastapi import APIRouter, Depends, HTTPException

from backend.models.news_post import NewsPost
from backend.models.pagination import EventPaginationParams
from backend.services.news_post import NewsPostService
from ...services import UserService, UserPermissionException
from ...models import User, Paginated, PaginationParams
from ..authentication import registered_user

openapi_tags = {
    "name": "(Admin) News",
    "description": "News administration end points.",
}

api = APIRouter(prefix="/api/admin/news")


@api.get("", tags=["(Admin) News"])
def list_posts(
    subject: User = Depends(registered_user),
    news_service: NewsPostService = Depends(),
    page: int = 0,
    page_size: int = 10,
    order_by: str = "headline",
    filter: str = "",
) -> Paginated[NewsPost]:
    """List posts via standard backend pagination query parameters."""
    try:
        pagination_params = EventPaginationParams(
            page=page, page_size=page_size, order_by=order_by, filter=filter
        )
        return news_service.get_paginated_posts(pagination_params, subject)
    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=str(e))
