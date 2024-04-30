"""
The News Post Service allows the API to manipulate news_posts data in the database.
"""

from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy import and_, exists, func, or_, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.entities.organization_entity import OrganizationEntity
from backend.entities.user_entity import UserEntity
from backend.models.organization_details import OrganizationDetails
from backend.models.pagination import EventPaginationParams, Paginated
from backend.models.user_details import UserDetails

from ..database import db_session

from ..models.news_post import NewsPost
from ..models.news_post_details import NewsPostDetails
from ..entities.news_post_entity import NewsPostEntity
from ..models import User

from .permission import PermissionService
from .exceptions import ResourceNotFoundException, UserPermissionException


class NewsPostService:

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
    ):
        """Initializes the `NewsPostService` session, and `PermissionService`"""
        self._session = session
        self._permission = permission


    def all(self, subject: User) -> list[NewsPostDetails]:

        self._permission.enforce(subject, "news_post.get", f"news_post")

        # Select all entries in `NewsPost` table
        query = select(NewsPostEntity)
        entities = self._session.scalars(query).all()

        return [entity.to_details_model() for entity in entities]

    def create(self, subject: User, news_post: NewsPost) -> NewsPostDetails:

        # Checks if the news_post already exists in the table
        if news_post.id:
            # Set id to None so database can handle setting the id
            news_post.id = None

        news_post.time = datetime.now()
        news_post.modification_date = datetime.now()

        # Otherwise, create new object
        news_post_entity = NewsPostEntity.from_model(news_post)

        # Attempt to add new object to table
        try:
            self._session.add(news_post_entity)
            self._session.commit()
        except IntegrityError:
            self._session.rollback()
            # If slug is not unique, retrieve the highest ID and append to slug
            latest_post = (
                self._session.query(NewsPostEntity)
                .order_by(NewsPostEntity.id.desc())
                .first()
        )
            if latest_post:
                new_slug = f"{news_post.slug}-{latest_post.id + 1}"
                news_post.slug = new_slug
                news_post_entity.slug = new_slug
                self._session.add(news_post_entity)
                self._session.commit()


        # Return added object
        return news_post_entity.to_details_model()

    def get_by_slug(self, slug: str) -> NewsPostDetails:

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
    

    def update(self, subject: User, news_post: NewsPost) -> NewsPostDetails:

        # news_post_entity = self._session.get(NewsPostEntity, news_post.id)

        if(not(news_post.author_id == subject.id and (news_post.state == 'draft' or news_post.state == 'incoming'))):
            self._permission.enforce(
            subject, "news_post.update", f"news_post/{news_post.slug}")
        

        obj = self._session.get(NewsPostEntity, news_post.id)

        # Check if result is null
        if obj is None:
            raise ResourceNotFoundException(
                f"No news post found with matching ID: {news_post.id}"
            )
        
        news_post.modification_date = datetime.now()

        # Update news_post object
        obj.id = news_post.id
        obj.headline = news_post.headline
        obj.slug = news_post.slug
        obj.main_story = news_post.main_story
        obj.author_id = news_post.author_id
        obj.organization_id = news_post.organization_id
        obj.state = news_post.state
        obj.image_url = news_post.image_url
        obj.time = news_post.time
        obj.modification_date = news_post.modification_date
        obj.synopsis = news_post.synopsis

        # Save changes
        self._session.commit()

        # Return updated object
        return obj.to_details_model()

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
    ) -> Paginated[NewsPostDetails]:

        statement = select(NewsPostEntity).where(NewsPostEntity.state.ilike("published"))
        length_statement = select(func.count()).select_from(NewsPostEntity).where(NewsPostEntity.state.ilike("published"))
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
                NewsPostEntity.synopsis.ilike(f"%{query}%"),
                NewsPostEntity.main_story.ilike(f"%{query}%"),
                exists().where(
                    OrganizationEntity.id == NewsPostEntity.organization_id,
                    OrganizationEntity.name.ilike(f"%{query}%"),
                ),
                exists().where(
                    OrganizationEntity.id == NewsPostEntity.organization_id,
                    OrganizationEntity.slug.ilike(f"%{query}%"),
                ),
                exists().where(
                    UserEntity.id == NewsPostEntity.author_id,
                    UserEntity.first_name.ilike(f"%{query}%"),
                ),
                exists().where(
                    UserEntity.id == NewsPostEntity.author_id,
                    UserEntity.last_name.ilike(f"%{query}%"),
                ),
                exists().where(
                    UserEntity.id == NewsPostEntity.author_id,
                    (UserEntity.first_name + ' ' + UserEntity.last_name).ilike(f"%{query}%"),
                ),
            )
            statement = statement.where(criteria)
            length_statement = length_statement.where(criteria)

        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size

        if pagination_params.order_by != "":
            statement = (
                statement.order_by(getattr(NewsPostEntity, pagination_params.order_by))
                # Changed so posts descend now
                if (not pagination_params.ascending or pagination_params.order_by == 'headline')
                else statement.order_by(
                    getattr(NewsPostEntity, pagination_params.order_by).desc()
                )
            )

        statement = statement.offset(offset).limit(limit)

        length = self._session.execute(length_statement).scalar()
        entities = self._session.execute(statement).scalars()

        return Paginated(
            items=[entity.to_details_model() for entity in entities],
            length=length,
            params=pagination_params,
        )


    def get_incoming(self, subject: User) -> list[NewsPostDetails]:

        # Check if user has admin permissions
        self._permission.enforce(subject, "news_post.incoming", f"news_post")

        # Select all entries in `NewsPost` table that represent incoming posts
        query = select(NewsPostEntity).where(NewsPostEntity.state.ilike("incoming"))
        entities = self._session.scalars(query).all()

        return [entity.to_details_model() for entity in entities]

    def get_drafts(self, subject: User) -> list[NewsPostDetails]:

        # Check if user has admin permissions
        self._permission.enforce(subject, "news_post.drafts", f"news_post")

        # Select all entries in `NewsPost` table that represent incoming posts
        query = select(NewsPostEntity).where(NewsPostEntity.state.ilike("draft"))
        entities = self._session.scalars(query).all()

        return [entity.to_details_model() for entity in entities]
    
    def get_published(self) -> list[NewsPostDetails]:

        # Select all entries in `NewsPost` table that represent incoming posts
        query = select(NewsPostEntity).where(NewsPostEntity.state.ilike("published"))
        entities = self._session.scalars(query).all()

        return [entity.to_details_model() for entity in entities]
    
    def get_archived(self, subject: User) -> list[NewsPostDetails]:

        # Check if user has admin permissions
        self._permission.enforce(subject, "news_post.archived", f"news_post")

        # Select all entries in `NewsPost` table that represent incoming posts
        query = select(NewsPostEntity).where(NewsPostEntity.state.ilike("archived"))
        entities = self._session.scalars(query).all()

        return [entity.to_details_model() for entity in entities]
    
    def get_posts_by_organization(
        self, organization: OrganizationDetails, subject: User | None = None
    ) -> list[NewsPostDetails]:
        """
        Get all the posts by an organization with id

        Args:
            slug: a valid str representing a unique Organization slug
            subject: The User making the request.

        Returns:
            list[NewsPostDetails]: a list of valid NewsPostDetail models
        """
        # Query the posts with matching organization id
        entities = (
            self._session.query(NewsPostEntity)
            .filter(NewsPostEntity.organization_id == organization.id)
            .where(NewsPostEntity.state.ilike("published"))
            .all()
        )

        # Convert entities to models and return
        return [entity.to_details_model() for entity in entities]
    
    def get_posts_by_user(
        self, author: User, subject: User | None = None
    ) -> list[NewsPostDetails]:
        """
        Get all the posts by a user with id

        Args:
            id: a valid int representing a unique User
            subject: The User making the request.

        Returns:
            list[NewsPostDetails]: a list of valid NewsPostDetail models
        """
        
        # Feature-specific authorization: User is getting their own registrations
        # Administrative Permission: user.event_registrations : user/{user_id}
        if subject.id != author.id:
            self._permission.enforce(
                subject,
                "user.posts",
                f"user/{author.id}",
            )

        # Query the posts with matching author id
        entities = (
            self._session.query(NewsPostEntity)
            .filter(NewsPostEntity.author_id == author.id)
            .where(NewsPostEntity.state.ilike("published"))
            .all()
        )

        # Convert entities to models and return
        return [entity.to_details_model() for entity in entities]
    
    def get_drafts_by_user(
        self, author: User, subject: User | None = None
    ) -> list[NewsPostDetails]:
        """
        Get all the drafts by a user with id

        Args:
            id: a valid int representing a unique User
            subject: The User making the request.

        Returns:
            list[NewsPostDetails]: a list of valid NewsPostDetail models
        """
        
        # Feature-specific authorization: User is getting their own registrations
        # Administrative Permission: user.event_registrations : user/{user_id}
        if subject.id != author.id:
            self._permission.enforce(
                subject,
                "user.posts",
                f"user/{author.id}",
            )

        # Query the posts with matching author id
        entities = (
            self._session.query(NewsPostEntity)
            .filter(NewsPostEntity.author_id == author.id)
            .where(NewsPostEntity.state.ilike("draft"))
            .all()
        )

        # Convert entities to models and return
        return [entity.to_details_model() for entity in entities]
    