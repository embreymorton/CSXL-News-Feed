"""
The News Post Service allows the API to manipulate news_posts data in the database.
"""

from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy import and_, exists, func, or_, select
from sqlalchemy.orm import Session

from backend.entities.organization_entity import OrganizationEntity
from backend.models.pagination import EventPaginationParams, Paginated

from ..database import db_session

from ..models.news_post import NewsPost
from ..models.news_post_details import NewsPostDetails
from ..entities.news_post_entity import NewsPostEntity
from ..models import User

from .permission import PermissionService
from .exceptions import ResourceNotFoundException


class NewsPostService:

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
    ):
        """Initializes the `NewsPostService` session, and `PermissionService`"""
        self._session = session
        self._permission = permission

    ## I mirrored this file after news_post.py
    ## In order to do this I had to make news_post_details and news_post_entity

    def all(self) -> list[NewsPost]:

        # Select all entries in `NewsPost` table
        query = select(NewsPostEntity)
        entities = self._session.scalars(query).all()

        print(entities)

        return [entity.to_model() for entity in entities]

    def create(self, subject: User, news_post: NewsPost) -> NewsPost:
        # Check if user has admin permissions
        self._permission.enforce(subject, "news_post.create", f"news_post")

        # Checks if the news_post already exists in the table
        if news_post.id:
            # Set id to None so database can handle setting the id
            news_post.id = None

        # Convert times to EST (hardcoded but could use pytz library)
        news_post.time = news_post.time - timedelta(hours=4)
        news_post.modification_date = news_post.modification_date - timedelta(hours=4)

        # Otherwise, create new object
        news_post_entity = NewsPostEntity.from_model(news_post)

        # Add new object to table and commit changes
        self._session.add(news_post_entity)
        self._session.commit()

        # Return added object
        return news_post_entity.to_model()

    def get_by_slug(self, slug: str) -> NewsPostDetails:
        """
        Get the news_post from a slug
        If none retrieved, a debug description is displayed.

        Parameters:
            slug: a string representing a unique news_post slug

        Returns:
            Organization: Object with corresponding slug

        Raises:
            ResourceNotFoundException if no news_post is found with the corresponding slug
        """

        # Query the news_post with matching slug
        news_post = (
            self._session.query(NewsPostEntity)
            .filter(NewsPostEntity.slug == slug)
            .one_or_none()
        )

        # Check if result is null
        if news_post is None:
            raise ResourceNotFoundException(
                f"No news_post found with matching slug: {slug}"
            )

        return news_post.to_details_model()

    def get_by_id(self, id: int, subject: User | None = None) -> NewsPostDetails:
        entity = self._session.get(NewsPostEntity, id)
        if entity is None:
            raise ResourceNotFoundException(f"No newspost found with matching ID: {id}")
        return entity.to_details_model(subject)

    def update(self, subject: User, news_post: NewsPost) -> NewsPost:

        # news_post_entity = self._session.get(NewsPostEntity, news_post.id)

        self._permission.enforce(
            subject, "news_post.update", f"news_post/{news_post.slug}"
        )

        obj = self._session.get(NewsPostEntity, news_post.id)

        # Check if result is null
        if obj is None:
            raise ResourceNotFoundException(
                f"No news post found with matching ID: {news_post.id}"
            )
        
        # Convert times to EST (hardcoded but could use pytz library)
        news_post.time = news_post.time - timedelta(hours=4)
        news_post.modification_date = news_post.modification_date - timedelta(hours=4)

        # Update news_post object
        obj.id = news_post.id
        obj.headline = news_post.headline
        obj.slug = news_post.slug
        obj.main_story = news_post.main_story
        obj.author = news_post.author
        obj.organization_id = news_post.organization_id
        obj.state = news_post.state
        obj.image_url = news_post.image_url
        obj.time = news_post.time
        obj.modification_date = news_post.modification_date
        obj.synopsis = news_post.synopsis

        # Save changes
        self._session.commit()

        # Return updated object
        return obj.to_model()

    def delete(self, subject: User, slug: str) -> None:
        # Check if user has admin permissions
        self._permission.enforce(subject, "news_post.delete", f"news_post")

        # Find object to delete
        obj = (
            self._session.query(NewsPostEntity)
            .filter(NewsPostEntity.slug == slug)
            .one_or_none()
        )

        # Ensure object exists
        if obj is None:
            raise ResourceNotFoundException(
                f"No news_post found with matching slug: {slug}"
            )

        # Delete object and commit
        self._session.delete(obj)
        # Save changes
        self._session.commit()

    def get_paginated_posts(
        self,
        pagination_params: EventPaginationParams,
        subject: User | None = None,
    ) -> Paginated[NewsPost]:
        """List Posts.

        Parameters:
            pagination_params: The pagination parameters.

        Returns:
            Paginated[Event]: The paginated list of events.
        """

        statement = select(NewsPostEntity)
        length_statement = select(func.count()).select_from(NewsPostEntity)
        if pagination_params.range_start != "":
            range_start = pagination_params.range_start
            range_end = pagination_params.range_end
            criteria = and_(
                NewsPostEntity.time
                >= datetime.strptime(range_start, "%d/%m/%Y, %H:%M:%S"),
                NewsPostEntity.time
                <= datetime.strptime(range_end, "%d/%m/%Y, %H:%M:%S"),
            )
            statement = statement.where(criteria)
            length_statement = length_statement.where(criteria)

        if pagination_params.filter != "":
            query = pagination_params.filter

            criteria = or_(
                NewsPostEntity.headline.ilike(f"%{query}%"),
                NewsPostEntity.main_story.ilike(f"%{query}%"),
                exists().where(
                    OrganizationEntity.id == NewsPostEntity.organization_id,
                    OrganizationEntity.name.ilike(f"%{query}%"),
                ),
                exists().where(
                    OrganizationEntity.id == NewsPostEntity.organization_id,
                    OrganizationEntity.slug.ilike(f"%{query}%"),
                ),
            )
            statement = statement.where(criteria)
            length_statement = length_statement.where(criteria)

        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size

        if pagination_params.order_by != "":
            statement = (
                statement.order_by(getattr(NewsPostEntity, pagination_params.order_by))
                if pagination_params.ascending
                else statement.order_by(
                    getattr(NewsPostEntity, pagination_params.order_by).desc()
                )
            )

        statement = statement.offset(offset).limit(limit)

        length = self._session.execute(length_statement).scalar()
        entities = self._session.execute(statement).scalars()

        return Paginated(
            items=[entity.to_model() for entity in entities],
            length=length,
            params=pagination_params,
        )
