import pytest
from sqlalchemy.orm import Session
from ....models.news_post import NewsPost
from ....entities.news_post_entity import NewsPostEntity

from .news_post_demo_data import date_maker
from ..user_data import root, ambassador, user
from ..organization.organization_test_data import appteam, cssg, cads

from ..reset_table_id_seq import reset_table_id_seq

jaysonsPost = NewsPost(
    id=1,
    headline="Jayson's News Post",
    main_story="Jayson's main story",
    author_id=root.id,
    organization_id=appteam.id,
    state="published",
    slug="slug1",
    image_url="none",
    time=date_maker(days_in_future=-1, hour=0, minutes=0),
    modification_date=date_maker(days_in_future=2, hour=10, minutes=0),
    synopsis="Jayson's synopsis",
)

treysPost = NewsPost(
    id=2,
    headline="Trey's News Post",
    main_story="Trey's main story",
    author_id=root.id,
    organization_id=cads.id,
    state="draft",
    slug="slug2",
    image_url="none",
    time=date_maker(days_in_future=-2, hour=0, minutes=0),
    modification_date=date_maker(days_in_future=-4, hour=15, minutes=0),
    synopsis="Trey's synopsis",
)

ishmaelsPost = NewsPost(
    id=3,
    headline="Ishmael's News Post",
    main_story="Ishmael's main story",
    author_id=ambassador.id,
    organization_id=cssg.id,
    state="incoming",
    slug="slug3",
    image_url="none",
    time=date_maker(days_in_future=-4, hour=15, minutes=0),
    modification_date=date_maker(days_in_future=-4, hour=15, minutes=0),
    synopsis="Ishmael's synopsis",
)

embreysPost = NewsPost(
    id=4,
    headline="Embrey's News Post",
    main_story="Embrey's main story",
    author_id=user.id,
    organization_id=appteam.id,
    state="archived",
    slug="slug4",
    image_url="none",
    time=date_maker(days_in_future=-2, hour=15, minutes=0),
    modification_date=date_maker(days_in_future=-4, hour=15, minutes=0),
    synopsis="Embrey's synopsis",
)

posts = [jaysonsPost, treysPost, embreysPost, ishmaelsPost]

to_add = NewsPost(
    id = None,
    headline="Created News Post",
    main_story="Created main story",
    author_id=user.id,
    organization_id=None,
    state="incoming",
    slug="slug4",
    image_url="none",
    time=date_maker(days_in_future=-4, hour=15, minutes=0),
    modification_date=date_maker(days_in_future=-4, hour=15, minutes=0),
    synopsis="Created synopsis",
)

to_update = NewsPost(
    id=4,
    headline="Embrey's News Post",
    main_story="Embrey's main story",
    author_id=user.id,
    organization_id=appteam.id,
    state="published",
    slug="slug4",
    image_url="none",
    time=date_maker(days_in_future=-4, hour=15, minutes=0),
    modification_date=date_maker(days_in_future=-4, hour=15, minutes=0),
    synopsis="Embrey's synopsis",
)

invalid_post = NewsPost(
    id=5,
    headline="Ishmael's News Post",
    main_story="Ishmael's main story",
    author_id=ambassador.id,
    organization_id=cssg.id,
    state="incoming",
    slug="invalid slug",
    image_url="none",
    time=date_maker(days_in_future=-4, hour=15, minutes=0),
    modification_date=date_maker(days_in_future=-4, hour=15, minutes=0),
    synopsis="Ishmael's synopsis",
)


published_embrey_post = NewsPost(
    id=4,
    headline="Embrey's News Post",
    main_story="Embrey's main story",
    author_id=user.id,
    organization_id=appteam.id,
    state="published",
    slug="slug4",
    image_url="none",
    time=date_maker(days_in_future=-2, hour=15, minutes=0),
    modification_date=date_maker(days_in_future=-4, hour=15, minutes=0),
    synopsis="Embrey's synopsis",
)

draft_ishmael_post = NewsPost(
    id=3,
    headline="Ishmael's News Post",
    main_story="Ishmael's main story",
    author_id=ambassador.id,
    organization_id=cssg.id,
    state="draft",
    slug="slug3",
    image_url="none",
    time=date_maker(days_in_future=-4, hour=15, minutes=0),
    modification_date=date_maker(days_in_future=-4, hour=15, minutes=0),
    synopsis="Ishmael's synopsis",
)

duplicate_treysPost = NewsPost(
    id=None,
    headline="Trey's News Post",
    main_story="Trey's main story",
    author_id=root.id,
    organization_id=cads.id,
    state="draft",
    slug="slug2",
    image_url="none",
    time=date_maker(days_in_future=-2, hour=0, minutes=0),
    modification_date=date_maker(days_in_future=-4, hour=15, minutes=0),
    synopsis="Trey's synopsis",
)


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
