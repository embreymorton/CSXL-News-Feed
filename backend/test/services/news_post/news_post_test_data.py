import pytest
from sqlalchemy.orm import Session
from ....models.news_post import NewsPost
from ....entities.news_post_entity import NewsPostEntity

from .news_post_demo_data import date_maker

from ..reset_table_id_seq import reset_table_id_seq

jaysonsPost = NewsPost(
    id=1,
    headline="Jayson's News Post",
    main_story="Jayson's main story",
    author="Jayson",
    organization_id=None,
    state="published",
    slug="slug1",
    image_url="none",
    time=date_maker(days_in_future=2, hour=10, minutes=0),
    modification_date=date_maker(days_in_future=2, hour=10, minutes=0),
    synopsis="Jayson's synopsis",
)

treysPost = NewsPost(
    id=2,
    headline="Trey's News Post",
    main_story="Trey's main story",
    author="Trey",
    organization_id=None,
    state="published",
    slug="slug2",
    image_url="none",
    time=date_maker(days_in_future=-4, hour=15, minutes=0),
    modification_date=date_maker(days_in_future=-4, hour=15, minutes=0),
    synopsis="Trey's synopsis",
)

treysPostupdate = NewsPost(
    id=2,
    headline="Trey's News Post Updated",
    main_story="Trey's main story Updated",
    author="Trey",
    organization_id=None,
    state="published",
    slug="slug2",
    image_url="none",
    time=date_maker(days_in_future=-4, hour=15, minutes=0),
    modification_date=date_maker(days_in_future=-4, hour=15, minutes=0),
    synopsis="Trey's synopsis",
)

treysPost_2_conflicting_id = NewsPost(
    id=3,
    headline="Trey's News Post 2",
    main_story="Trey's main story 2",
    author="Trey",
    organization_id=None,
    state="published",
    slug="slug4",
    image_url="none",
    time=date_maker(days_in_future=-4, hour=15, minutes=0),
    modification_date=date_maker(days_in_future=-4, hour=15, minutes=0),
    synopsis="Trey's synopsis 2",
)

posts = [jaysonsPost, treysPost, treysPost_2_conflicting_id]
posts_names = [
    jaysonsPost.author,
    treysPost.author,
    treysPost_2_conflicting_id.author,
]


def insert_fake_data(session: Session):
    """Insert fake newspost data into the test session."""

    global posts
    # create entities for test newspost data
    entities = []
    for pos in posts:
        entity = NewsPostEntity.from_model(pos)
        session.add(entity)
        entities.append(entity)

    # Reset table IDS to prevent ID conflicts
    reset_table_id_seq(session, NewsPostEntity, NewsPostEntity.id, len(posts) + 1)

    # Commit all changes
    session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
