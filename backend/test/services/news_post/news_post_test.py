"""Test for NewsPostService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

from backend.api.coworking import ambassador
from backend.models.pagination import EventPaginationParams
from backend.services.exceptions import (
    UserPermissionException,
    ResourceNotFoundException,
)
from backend.test.services.news_post.news_post_demo_data import date_maker
from ..organization.organization_test_data import appteam

from ....models import NewsPost
from ....services import NewsPostService

from ..fixtures import newspost_svc_integration
from ..core_data import setup_insert_data_fixture

from .news_post_test_data import (
    posts,
    treysPost,
    jaysonsPost,
    ishmaelsPost,
    embreysPost,
    to_add,
    to_update,
    invalid_post,
    published_embrey_post,
    draft_ishmael_post,
    duplicate_treysPost
)
from ..user_data import root, user, ambassador


def test_get_all(newspost_svc_integration: NewsPostService):
    """Test that all posts can be retrieved by an admin."""
    fetched_posts = newspost_svc_integration.all(root)
    assert fetched_posts is not None
    assert len(fetched_posts) == len(posts)
    assert isinstance(fetched_posts[0], NewsPost)
    assert fetched_posts[0].headline == "Jayson's News Post"
    assert fetched_posts[1].headline == "Trey's News Post"
    assert fetched_posts[2].headline == "Embrey's News Post"
    assert fetched_posts[3].headline == "Ishmael's News Post"


def test_get_published(newspost_svc_integration: NewsPostService):
    """Test that published posts can be retrieved."""
    fetched_posts = newspost_svc_integration.get_published()
    assert fetched_posts is not None
    assert len(fetched_posts) == 1
    assert isinstance(fetched_posts[0], NewsPost)
    assert fetched_posts[0].id == jaysonsPost.id


def test_get_incoming_as_root(newspost_svc_integration: NewsPostService):
    """Test that incoming posts can be retrieved."""
    fetched_posts = newspost_svc_integration.get_incoming(root)
    assert fetched_posts is not None
    assert len(fetched_posts) == 1
    assert isinstance(fetched_posts[0], NewsPost)
    assert fetched_posts[0].id == ishmaelsPost.id


def test_get_archived_as_root(newspost_svc_integration: NewsPostService):
    """Test that archived posts can be retrieved."""
    fetched_posts = newspost_svc_integration.get_archived(root)
    assert fetched_posts is not None
    assert len(fetched_posts) == 1
    assert isinstance(fetched_posts[0], NewsPost)
    assert fetched_posts[0].id == embreysPost.id


def test_get_drafts_as_root(newspost_svc_integration: NewsPostService):
    """Test that drafts can be retrieved."""
    fetched_posts = newspost_svc_integration.get_drafts(root)
    assert fetched_posts is not None
    assert len(fetched_posts) == 1
    assert isinstance(fetched_posts[0], NewsPost)
    assert fetched_posts[0].id == treysPost.id


def test_get_incoming_as_user(newspost_svc_integration: NewsPostService):
    """Test that incoming posts *cannot* be retrieved by a user."""
    with pytest.raises(UserPermissionException):
        newspost_svc_integration.get_incoming(user)


def test_get_archived_as_user(newspost_svc_integration: NewsPostService):
    """Test that archived posts *cannot* be retrieved by a user."""
    with pytest.raises(UserPermissionException):
        newspost_svc_integration.get_archived(user)


def test_get_drafts_as_user(newspost_svc_integration: NewsPostService):
    """Test that drafts posts *cannot* be retrieved by a user."""
    with pytest.raises(UserPermissionException):
        newspost_svc_integration.get_drafts(user)


def test_get_by_slug(newspost_svc_integration: NewsPostService):
    """Test that newspost can be retrieved based on their slug."""
    fetched_post = newspost_svc_integration.get_by_slug(jaysonsPost.slug)
    assert fetched_post is not None
    assert isinstance(fetched_post, NewsPost)
    assert fetched_post.slug == jaysonsPost.slug
    assert fetched_post.id == jaysonsPost.id


def test_create_post_as_root(newspost_svc_integration: NewsPostService):
    """Test that the root user is able to create new posts."""
    created_post = newspost_svc_integration.create(root, to_add)
    assert created_post is not None
    assert created_post.id is not None
    assert created_post.headline == "Created News Post"
    assert created_post.state == "incoming"


def test_create_post_as_user(newspost_svc_integration: NewsPostService):
    """Test that any user is able to create new posts."""
    created_post = newspost_svc_integration.create(user, to_add)
    assert created_post is not None
    assert created_post.id is not None
    assert created_post.headline == "Created News Post"
    assert created_post.state == "incoming"
    

def test_create_post_same_slug(newspost_svc_integration: NewsPostService):
    """Test that a post created with a duplicate slug will change the new slug."""
    created_post = newspost_svc_integration.create(root, duplicate_treysPost)
    assert created_post is not None
    assert created_post.id is not None
    assert created_post.slug != treysPost.slug


def test_update_post_as_root(
    newspost_svc_integration: NewsPostService,
):
    """Test that the root user is able to update post.
    Note: Test data's synopsis field is updated
    """
    newspost_svc_integration.update(root, to_update)
    assert newspost_svc_integration.get_by_slug('slug4').organization_id == 3
    assert newspost_svc_integration.get_by_slug('slug4').state == "published"


def test_update_published_post_as_user(newspost_svc_integration: NewsPostService):
    """Test that any user is *unable* to update posts."""
    with pytest.raises(UserPermissionException):
        newspost_svc_integration.update(user, to_update)


def test_update_on_invalid_event(newspost_svc_integration: NewsPostService):
    """Test that attempting to update a nonexistent post raises an exception."""
    with pytest.raises(ResourceNotFoundException):
        newspost_svc_integration.update(root, invalid_post)


def test_delete_post_as_root(newspost_svc_integration: NewsPostService):
    """Test that the root user is able to delete posts."""
    newspost_svc_integration.delete(root, jaysonsPost.slug)
    with pytest.raises(ResourceNotFoundException):
        newspost_svc_integration.get_by_slug(jaysonsPost.slug)


def test_delete_enforces_permission(newspost_svc_integration: NewsPostService):
    """Test that the service enforces permissions when attempting to delete a post."""

    # Setup to test permission enforcement on the PermissionService.
    newspost_svc_integration._permission = create_autospec(
        newspost_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    newspost_svc_integration.delete(root, ishmaelsPost.slug)
    newspost_svc_integration._permission.enforce.assert_called_with(
        root, "news_post.delete", f"news_post"
    )


def test_delete_post_as_user(newspost_svc_integration: NewsPostService):
    """Test that any user is *unable* to delete posts."""
    with pytest.raises(UserPermissionException):
        newspost_svc_integration.delete(user, ishmaelsPost.slug)


def test_delete_on_invalid_event(newspost_svc_integration: NewsPostService):
    """Test that attempting to delete a nonexistent post raises an exception."""
    with pytest.raises(ResourceNotFoundException):
        newspost_svc_integration.delete(root, invalid_post.slug)


def test_get_posts_by_organization(newspost_svc_integration: NewsPostService):
    """Test that published posts by an organization can be retrieved."""
    fetched_posts = newspost_svc_integration.get_posts_by_organization(appteam)
    assert fetched_posts is not None
    assert len(fetched_posts) == 1
    assert isinstance(fetched_posts[0], NewsPost)
    assert fetched_posts[0].id == jaysonsPost.id


def test_get_posts_by_same_user(newspost_svc_integration: NewsPostService):
    """Test that published posts by a user can be retrieved by the same user."""
    newspost_svc_integration.update(root, published_embrey_post)
    fetched_posts = newspost_svc_integration.get_posts_by_user(user, user)
    assert fetched_posts is not None
    assert len(fetched_posts) == 1
    assert isinstance(fetched_posts[0], NewsPost)
    assert fetched_posts[0].id == embreysPost.id


def test_get_posts_by_user_as_root(newspost_svc_integration: NewsPostService):
    """Test that published posts by a user can be retrieved by the root."""
    newspost_svc_integration.update(root, published_embrey_post)
    fetched_posts = newspost_svc_integration.get_posts_by_user(user, root)
    assert fetched_posts is not None
    assert len(fetched_posts) == 1
    assert isinstance(fetched_posts[0], NewsPost)
    assert fetched_posts[0].id == embreysPost.id


def test_get_posts_by_wrong_user(newspost_svc_integration: NewsPostService):
    """Test that the service enforces permissions when attempting to get posts from different user."""

    # Setup to test permission enforcement on the PermissionService.
    newspost_svc_integration._permission = create_autospec(
        newspost_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    newspost_svc_integration.get_posts_by_user(root, user)
    newspost_svc_integration._permission.enforce.assert_called_with(
        user, "user.posts", f"user/{root.id}"
    )


def test_get_drafts_by_same_user(newspost_svc_integration: NewsPostService):
    """Test that drafts by a user can be retrieved by the same user."""
    newspost_svc_integration.update(root, draft_ishmael_post)
    fetched_posts = newspost_svc_integration.get_drafts_by_user(ambassador, ambassador)
    assert fetched_posts is not None
    assert len(fetched_posts) == 1
    assert isinstance(fetched_posts[0], NewsPost)
    assert fetched_posts[0].id == ishmaelsPost.id


def test_get_drafts_by_user_as_root(newspost_svc_integration: NewsPostService):
    """Test that drafts by a user can be retrieved by the root."""
    newspost_svc_integration.update(root, draft_ishmael_post)
    fetched_posts = newspost_svc_integration.get_drafts_by_user(ambassador, root)
    assert fetched_posts is not None
    assert len(fetched_posts) == 1
    assert isinstance(fetched_posts[0], NewsPost)
    assert fetched_posts[0].id == ishmaelsPost.id


def test_get_drafts_by_wrong_user(newspost_svc_integration: NewsPostService):
    """Test that the service enforces permissions when attempting to get drafts from different user."""

    # Setup to test permission enforcement on the PermissionService.
    newspost_svc_integration._permission = create_autospec(
        newspost_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    newspost_svc_integration.get_drafts_by_user(ambassador, user)
    newspost_svc_integration._permission.enforce.assert_called_with(
        user, "user.posts", f"user/{ambassador.id}"
    )


def test_list(newspost_svc_integration: NewsPostService):
    """Test that a paginated list of published posts can be produced by a signed in user."""
    newspost_svc_integration.update(root, published_embrey_post)
    pagination_params = EventPaginationParams(
        order_by="id",
        range_start=date_maker(days_in_future=-3, hour=0, minutes=0).strftime(
            "%d/%m/%Y, %H:%M:%S"
        ),
        range_end=date_maker(days_in_future=0, hour=0, minutes=0).strftime(
            "%d/%m/%Y, %H:%M:%S"
        ),
    )
    fetched_posts = newspost_svc_integration.get_paginated_posts(
        pagination_params, ambassador
    )
    assert len(fetched_posts.items) == 2


def test_list_unauthenticated(newspost_svc_integration: NewsPostService):
    """Test that a paginated list of published posts can be produced by an unauthenticated user."""
    newspost_svc_integration.update(root, published_embrey_post)
    pagination_params = EventPaginationParams(
        order_by="id",
        range_start=date_maker(days_in_future=-3, hour=0, minutes=0).strftime(
            "%d/%m/%Y, %H:%M:%S"
        ),
        range_end=date_maker(days_in_future=0, hour=0, minutes=0).strftime(
            "%d/%m/%Y, %H:%M:%S"
        ),
    )
    fetched_posts = newspost_svc_integration.get_paginated_posts(pagination_params)
    assert len(fetched_posts.items) == 2


def test_list_filter(newspost_svc_integration: NewsPostService):
    """Test that a paginated list of posts can be produced."""

    newspost_svc_integration.update(root, published_embrey_post)
    pagination_params = EventPaginationParams(filter="main story")
    fetched_events = newspost_svc_integration.get_paginated_posts(
        pagination_params, ambassador
    )
    assert len(fetched_events.items) == 2
