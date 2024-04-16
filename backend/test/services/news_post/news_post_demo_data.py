"""Contains the mock data for the live demo of the news post create feature"""

from datetime import datetime, timedelta
import pytest
from sqlalchemy.orm import Session
from ....models.news_post import NewsPost
from ....entities.news_post_entity import NewsPostEntity

from ..reset_table_id_seq import reset_table_id_seq

import datetime

def date_maker(days_in_future: int, hour: int, minutes: int) -> datetime.datetime:
    """
    Creates a new `datetime` object relative to the current day when the
    data is reset using a reset script.

    Parameters:
        days_in_future (int): Number of days in the future from the current day to set the date
        hour (int): Which hour of the day to set the `datetime`, using the 24 hour clock
        minutes (int): Which minute to set the `datetime`

    Returns:
        datetime: `datetime` object to use in events test data.
    """
    # Find the date and time at the moment the script is run
    now = datetime.datetime.now()
    # Set the date and time to 12:00AM of that day
    current_day = datetime.datetime(now.year, now.month, now.day)
    # Create a delta containing the offset for which to move the current date
    timedelta = datetime.timedelta(days=days_in_future, hours=hour, minutes=minutes)
    # Create the new date object offset by `timedelta`
    new_date = current_day + timedelta
    # Returns the new date
    return new_date

# Sample Data Objects

jaysonsPost = NewsPostEntity(
    id=1,
    headline="Jayson's News Post",
    main_story="Jayson's main story",
    author="Jayson",
    organization_id=None,
    state="published",
    slug="slug1",
    image_url="none",
    time= date_maker(days_in_future=2, hour=10, minutes=0),
    modification_date=date_maker(days_in_future=2, hour=10, minutes=0),
    synopsis="Jayson's synopsis",
)

treysPost = NewsPostEntity(
    id=2,
    headline="Trey's News Post",
    main_story="Trey's main story",
    author="Trey",
    organization_id=None,
    state="published",
    slug="slug2",
    image_url="none",
    time= date_maker(days_in_future=-4, hour=15, minutes=0),
    modification_date=date_maker(days_in_future=-4, hour=15, minutes=0),
    synopsis="Trey's synopsis",
)

ishmaelsPost = NewsPostEntity(
    id=3,
    headline="Ishmael's News Post",
    main_story="Ishmael's main story",
    author="Ishmael",
    organization_id=None,
    state="published",
    slug="slug3",
    image_url="none",
    time= date_maker(days_in_future=-4, hour=7, minutes=0),
    modification_date=date_maker(days_in_future=-4, hour=7, minutes=0),
    synopsis="Ishmael's synopsis",
)

embreysPost = NewsPostEntity(
    id=4,
    headline="Embrey's News Post",
    main_story="Embrey's main story",
    author="Embrey",
    organization_id=None,
    state="published",
    slug="slug4",
    image_url="none",
    time= date_maker(days_in_future=-16, hour=23, minutes=0),
    modification_date=date_maker(days_in_future=-16, hour=23, minutes=0),
    synopsis="Embrey's synopsis",
)

comp290 = NewsPostEntity(
    id=5,
    headline="COMP 290 Essential Tools for Computer Science",
    main_story="A section has been added to our registration guide (see here: https://cs.unc.edu/undergraduate/) about a new offering (see below). \n This course introduces students to essential computer science tools and technologies not taught in other classes. By the end of this course, students will expand their computer science toolbelt and be well-prepared for taking upper-division computer science classes and personal projects. \n Students can request enrollment to the class by accessing this form: https://go.unc.edu/comp290-24f-interest \n There is more information about the class on the form if you are interested in checking it out. The target audience for this class will be students who will be enrolled in, or just past, COMP 210 next semester!",
    author="Ketan Mayer-Patel",
    organization_id=None,
    state="published",
    slug="slug5",
    image_url="none",
    time= date_maker(days_in_future=1, hour=12, minutes=0),
    modification_date=date_maker(days_in_future=1, hour=12, minutes=0),
    synopsis="New addition to Fall 2024 schedule",
)

posts = [jaysonsPost, treysPost, ishmaelsPost, embreysPost, comp290]


def insert_fake_data(session: Session):
    """Inserts fake organization data into the test session."""

    global posts

    # Create entities for test organization data
    entities = []
    for post in posts:
        entity = NewsPostEntity.from_model(post)
        session.add(entity)
        entities.append(entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(session, NewsPostEntity, NewsPostEntity.id, len(posts) + 1)

    # Commit all changes
    session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    """Insert fake data the session automatically when test is run.
    Note:
        This function runs automatically due to the fixture property `autouse=True`.
    """
    insert_fake_data(session)
    session.commit()
    yield