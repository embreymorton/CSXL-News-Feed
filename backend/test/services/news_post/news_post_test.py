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

from ....models import NewsPost
from ....services import NewsPostService

from ..fixtures import newspost_svc_integration
from ..core_data import setup_insert_data_fixture

from .news_post_test_data import (
    posts,
    treysPost,
    jaysonsPost,
    treysPostupdate,
    treysPost_2_conflicting_id,
)
from ..user_data import root, user


# Test `NewsPostService.all()`
def test_get_all(newspost_svc_integration: NewsPostService):
    """Test that all posts can be retrieved."""
    fetched_posts = newspost_svc_integration.all()
    assert fetched_posts is not None
    assert len(fetched_posts) == len(posts)
    assert isinstance(fetched_posts[0], NewsPost)


# Test `NewsPostService.get_by_id()`
def test_get_by_slug(newspost_svc_integration: NewsPostService):
    """Test that newspost can be retrieved based on their ID."""
    fetched_posts = newspost_svc_integration.get_by_slug(jaysonsPost.slug)
    assert fetched_posts is not None
    assert isinstance(fetched_posts, NewsPost)
    assert fetched_posts.slug == jaysonsPost.slug


def test_create_post_as_root(newspost_svc_integration: NewsPostService):
    """Test that the root user is able to create new organizations."""
    created_newpost = newspost_svc_integration.create(root, jaysonsPost)
    assert created_newpost is not None
    assert created_newpost.id is not None


def test_update_newspost_as_root(
    newspost_svc_integration: NewsPostService,
):
    """Test that the root user is able to update post.
    Note: Test data's synopsis field is updated
    """
    newspost_svc_integration.update(root, treysPostupdate)
    assert (
        newspost_svc_integration.get_by_slug("slug2").headline
        == "Trey's News Post Updated"
    )


def test_delete_newspost_as_root(newspost_svc_integration: NewsPostService):
    """Test that the root user is able to delete posts."""
    newspost_svc_integration.delete(root, jaysonsPost.slug)
    with pytest.raises(ResourceNotFoundException):
        newspost_svc_integration.get_by_slug(jaysonsPost.slug)


def test_list(newspost_svc_integration: NewsPostService):
    """Test that a paginated list of events can be produced."""
    pagination_params = EventPaginationParams(
        order_by="id",
        range_start=date_maker(days_in_future=1, hour=10, minutes=0).strftime(
            "%d/%m/%Y, %H:%M:%S"
        ),
        range_end=date_maker(days_in_future=2, hour=10, minutes=0).strftime(
            "%d/%m/%Y, %H:%M:%S"
        ),
    )
    fetched_events = newspost_svc_integration.get_paginated_posts(
        pagination_params, ambassador
    )
    assert len(fetched_events.items) == 1
