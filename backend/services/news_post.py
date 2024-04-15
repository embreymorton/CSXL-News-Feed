"""
The News Post Service allows the API to manipulate organizations data in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import db_session

from ..models.news_post import NewsPost
from ..models import User

from .permission import PermissionService

class NewsPostService:
    
    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
    ):
        """Initializes the `NewsPostService` session, and `PermissionService`"""
        self._session = session
        self._permission = permission

    
    def all(self) -> list[NewsPost]:
        return None

    def create(self, subject: User, news_post: NewsPost) -> NewsPost:
        return None
    
    def update(self, subject: User, news_post: NewsPost) -> NewsPost:
        return None
    
    def delete(self, subject: User, id: int) -> None:
        return None

