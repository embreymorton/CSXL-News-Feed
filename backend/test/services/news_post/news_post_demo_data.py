"""Contains the mock data for the live demo of the news post create feature"""

from datetime import datetime, timedelta
import pytest
from sqlalchemy.orm import Session
from ....models.news_post import NewsPost
from ....entities.news_post_entity import NewsPostEntity
from ..organization.organization_demo_data import appteam, cssg, pearlhacks, bit
from ..user_data import root, ambassador, user

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
    author_id=root.id,
    organization_id=appteam.id,
    state="archived",
    slug="slug1",
    image_url=None,
    time= date_maker(days_in_future=-8, hour=10, minutes=0),
    modification_date=date_maker(days_in_future=-8, hour=10, minutes=0),
    synopsis="Jayson's synopsis",
)

treysPost = NewsPostEntity(
    id=2,
    headline="Trey's News Post",
    main_story="Trey's main story",
    author_id=root.id,
    organization_id=None,
    state="incoming",
    slug="slug2",
    image_url=None,
    time= date_maker(days_in_future=-12, hour=15, minutes=0),
    modification_date=date_maker(days_in_future=-12, hour=15, minutes=0),
    synopsis="Trey's synopsis",
)

ishmaelsPost = NewsPostEntity(
    id=3,
    headline="Ishmael's News Post",
    main_story="Ishmael's main story",
    author_id=user.id,
    organization_id=cssg.id,
    state="archived",
    slug="slug3",
    image_url=None,
    time= date_maker(days_in_future=-13, hour=7, minutes=0),
    modification_date=date_maker(days_in_future=-4, hour=7, minutes=0),
    synopsis="Ishmael's synopsis",
)

embreysPost = NewsPostEntity(
    id=4,
    headline="Embrey's News Post",
    main_story="Embrey's main story",
    author_id=ambassador.id,
    organization_id=None,
    state="incoming",
    slug="slug4",
    image_url=None,
    time= date_maker(days_in_future=-16, hour=23, minutes=0),
    modification_date=date_maker(days_in_future=-16, hour=23, minutes=0),
    synopsis="Embrey's synopsis",
)

comp290 = NewsPostEntity(
    id=5,
    headline="COMP 290 Essential Tools for Computer Science",
    main_story="A section has been added to our registration guide (see here: https://cs.unc.edu/undergraduate/) about a new offering (see below). \n This course introduces students to essential computer science tools and technologies not taught in other classes. By the end of this course, students will expand their computer science toolbelt and be well-prepared for taking upper-division computer science classes and personal projects. \n Students can request enrollment to the class by accessing this form: https://go.unc.edu/comp290-24f-interest \n There is more information about the class on the form if you are interested in checking it out. The target audience for this class will be students who will be enrolled in, or just past, COMP 210 next semester!",
    author_id=ambassador.id,
    organization_id=None,
    state="published",
    slug="slug5",
    image_url=None,
    time= date_maker(days_in_future=-10, hour=12, minutes=0),
    modification_date=date_maker(days_in_future=-1, hour=12, minutes=0),
    synopsis="New addition to Fall 2024 schedule",
)

dth = NewsPostEntity(
    id=6,
    headline="Daily Tar Heel News Engineering Team",
    main_story="I'm Leo, a junior at UNC who works with the Daily Tar Heel on engineering and data projects. Starting this upcoming fall 2024 semester, I will be leading the DTH's first-of-its-kind engineering team! Could you please share the following information with Computer Science students? This new team will work on various news engineering projects to support the DTH. This includes developing multimedia news articles, building full-stack web applications, and generally supporting DTH journalism with technology! We are looking for interested students who have some experience building web products. Specifically, you should have previous experience working with the web and preferably modern web frameworks like React, Svelte, Angular, etc. Although we are seeking students with some experience, the DTH fundamentally emphasizes learning and experimentation, so you do not need to be an expert! The application will open in July and we are looking to bring on ~5 members for the first cohort of this team. This is a great opportunity for anyone looking to gain real world software engineering experience. If you have any questions, please reach out to me at ldavidson@unc.edu. If interested in hearing more, please fill out the interest form: https://form.jotform.com/241016791261047 Information Session: 4/25/2024 at 5:30 pm (over Zoom: https://unc.zoom.us/j/92758756140) News Engineering: A sub-field of software engineering focused on leveraging technology to support journalism.",
    author_id=user.id,
    organization_id=None,
    state="published",
    slug="slug6",
    image_url="https://www.jotform.com/uploads/Leo_Davidson/form_files/dth-masthead.661865a6ed5f53.52336186.png",
    time=date_maker(days_in_future=-4, hour=15, minutes=35),
    modification_date=date_maker(days_in_future=-3, hour=1, minutes=35),
    synopsis="News Engineering: A sub-field of software engineering focused on leveraging technology to support journalism."
)

nlp = NewsPostEntity(
    id=7,
    headline="SLAE NLP Hackathon Interest Form",
    main_story="AI@UNC is announcing a Natural Language Processing competition with $700 in cash prizes ($350 top prize) . The goal is to find the best LLM prompt or NLP pipeline to take a list of papers and related claims as input, and output how the paper supports/does not support the relations. Finer details will be released during the StatQuest event on April 16th at 5:30pm. Anyone with the ability to prompt engineers should be able to engage with this competition by editing a base template. You might need to run some code, but you don’t need to worry about what it does. More advanced users can opt to build their own pipelines. Sign up and see more details here: [https://docs.google.com/forms/d/e/1FAIpQLSejtakt61HtMeYBZkXyr26w9-FA_K3nR7DZOH2hiIzgbLkFKg/viewform?usp=sf_link]",
    author_id=root.id,
    organization_id=None,
    state="published",
    slug="slug7",
    image_url=None,
    time=date_maker(days_in_future=-13, hour=10, minutes=42),
    modification_date=date_maker(days_in_future=-3, hour=1, minutes=35),
    synopsis="AI@UNC is announcing a Natural Language Processing competition with $700 in cash prizes ($350 top prize)."
)

cOne = NewsPostEntity(
    id=8,
    headline="Capital One Lunch and Learn",
    main_story="My name is Nathan, and I'm the treasurer for UNC's National Society of Black Engineers (NSBE) club. We're having an event with Capital One, where we're partnering with UNC clubs ALPFA and BBSA. We'd love if you could promote this event in the CS newsletter or list serv. The event link is here, registration on the link is required to attend: https://capitalone.eightfold.ai/events/candidate?plannedEventId=o7jj9Vn7",
    author_id=root.id,
    organization_id=None,
    state="published",
    slug="slug8",
    image_url=None,
    time=date_maker(days_in_future=-2, hour=19, minutes=13),
    modification_date=date_maker(days_in_future=-2, hour=3, minutes=36),
    synopsis="You'll learn more about our hiring process while also enjoying lunch and great conversation with our associates"
)

fidHack = NewsPostEntity(
    id=9,
    headline="Fidelity's Hackathon Application Due Friday",
    main_story="FidHacks\nFidelity is hosting a two-day hackathon highlighting and celebrating first-year college women. Get paired with like-minded students to solve hacking problems and experience our culture firsthand.\nWho\nOpen to all first-year students enrolled full-time in college or university.\nWhen\nThursday, May 16th 8:30am to Friday, May 17th 3pm EST\nWhere\nFidelity Investments regional campus*\n100 New Millennium Way Durham, NC 27709\n*Participants must secure their own transportation to/from Durham. Thursday night lodging accommodations and meals will be provided.\nWhy\nFidHacks is designed to promote equal opportunity, inclusion, and access in financial services technology.\nApply at this link: https://fmr.co1.qualtrics.com/jfe/form/SV_0DofUfOqrHCHGCi (due date this Friday, April 12, not what's listed on form)",
    author_id=ambassador.id,
    organization_id=None,
    state="published",
    slug="slug9",
    image_url=None,
    time=date_maker(days_in_future=-5, hour=15, minutes=51),
    modification_date=date_maker(days_in_future=-2, hour=3, minutes=36),
    synopsis="Fidelity is hosting a two-day hackathon highlighting and celebrating first-year college women"
)

csSg = NewsPostEntity(
    id=10,
    headline="Apply to the CS+SG Team Today",
    main_story="Hello Students!\nWe hope you're enjoying the spring semester and are ready for an exciting opportunity! Computer Science + Social Good (CS+SG) is thrilled to announce that applications for our Executive, Project, and Education Teams are now open until April 14th!\nAre you passionate about making a positive impact through technology and eager to collaborate with like-minded individuals? We're seeking dedicated individuals to join our teams to drive our mission forward.\nExecutive Team: Shape the direction of our organization, plan and execute impactful initiatives, and foster a community dedicated to leveraging technology for social good.\nEducation Team: Work on a semester-long project led by our Project Team Leads, learning skills such as JavaScript, HTML/CSS, Next.js (a React framework), and Supabase. No prior knowledge required—just a genuine interest and commitment to learning.\nProject Teams: Gain hands-on experience and build skills for your resume by joining one of our project teams.\nWhether you're interested in project management, event planning, marketing, or community outreach, there's a place for you on our team!\nApply now by filling out the application form linked below. Don't miss out on this opportunity to make a difference in your community and develop invaluable leadership skills. Applications close on April 14th at 11:59 PM EST.\nAs a member of CS+SG, you can look forward to a variety of exciting events and opportunities throughout the semester, including:\nNetworking Events: Connect with industry professionals and fellow students passionate about technology and social impact.\nWorkshops and Skill-Building Sessions: Enhance your skills and expand your knowledge through hands-on workshops and interactive sessions.\nSocial Events: Unwind and have fun with your fellow members at our social gatherings, complete with food, drinks, and good company!\nJoining CS+SG isn't just about building your resume—it's about joining a community of like-minded individuals committed to making a difference in the world.\nIf you have any questions or need further information, please don't hesitate to reach out to us. We're here to help!\nAgain, here are the application links:\nExecutive application: https://forms.gle/L9auFoqxSuHXaK6a6\nNew Member application: https://forms.gle/H6HTmLZE86VpheFU7\nDon't miss out on this opportunity to be part of something meaningful. We can't wait to welcome you to the CS+SG family!\nBest regards,\nThe CS+SG Executive Team",
    author_id=user.id,    
    organization_id=cssg.id,
    state="published",
    slug="slug10",
    image_url=None,
    time=date_maker(days_in_future=-3, hour=8, minutes=36),
    modification_date=date_maker(days_in_future=-5, hour=3, minutes=36),
    synopsis="We're seeking dedicated individuals to join our teams to drive our mission forward."
)

aIapp = NewsPostEntity(
    id=11,
    headline="AI@UNC Major Workshop with StatQuest and Officer Team Applications",
    main_story="Hello, I'm Hanqi, Co-president of AI@UNC. We are hosting a workshop with StatQuest, a well-known educational youtuber with over 1 million subscribers. In this workshop students will have the opportunity to train from scratch an AI model with the same architecture as ChatGPT. The workshop will begin at 5:30 pm and end at 7:00 pm. Then, a related two-day NLP competition with prizes will be announced and food will be served.\nThe workshop is open to all students with at least a basic understanding of programming (COMP 110 or COMP 116 recommended). Also, the workshop does not assume any prior knowledge of machine learning (ML), but this playlist of videos can be helpful to any participants who want extra preparation. To save your spot, use this official link: [https://forms.gle/eJny44Ga3t4t7aN1A]",
    author_id=user.id,
    organization_id=None,
    state="published",
    slug="slug11",
    image_url=None,
    time=date_maker(days_in_future=-8, hour=14, minutes=28),
    modification_date=date_maker(days_in_future=-5, hour=3, minutes=36),
    synopsis="We are hosting a workshop with StatQuest"
)

pearlApp = NewsPostEntity(
    id=12,
    headline="[DEADLINE EXTENDED] Apply to be a Director for Pearl Hacks 2025!",
    main_story="Want to be involved in organizing Pearl Hacks 2025?\nApply now to join the Pearl Hacks 2025 Board! NO COMPUTER SCIENCE EXPERIENCE REQUIRED. People of all genders and majors are welcome to apply, but you must be a UNC student.\nPearl Hacks is where you can help under-represented people, specifically women and gender non conforming students, pursue their interests in technology. Pearl Hacks is a growing organization, looking for motivated students like you to take Pearl Hacks to newer heights. Your work will directly impact the experience of hundreds of people from across the US.\nBeing a director of Pearl Hacks may seem like big shoes to fill, but all of us start out the same way! Our current directors will mentor you and help you with any questions you may have.\nIf you are selected for an interview, we will be in touch regarding interview scheduling and indicating director role preferences. They will be held at some time during the week of April 8th-April 16th.  Thank you for being patient with us!\nDEADLINE: Tuesday, April 2nd, 2024 11:59 PM EST\nAPPLY AT THIS LINK: Director Application\nTake a look at the 2025 Board structure + position descriptions here: bit.ly/PH25BOARD. You will be able to choose your top 3 preferred positions if you are selected for an interview!",
    author_id=ambassador.id,
    organization_id=pearlhacks.id,
    state="published",
    slug="slug12",
    image_url=None,
    time=date_maker(days_in_future=-2, hour=8, minutes=19),
    modification_date=date_maker(days_in_future=-5, hour=3, minutes=36),
    synopsis="Apply now to join the Pearl Hacks 2025 Board!"
)

rjDavis = NewsPostEntity(
    id=13,
    headline="RJ Davis to Return to Tar Heels for 5th Season",
    main_story="Tar Heels guard RJ Davis is on board to return to school for a fifth season rather than enter the 2024 NBA draft, according to CBS Sports' Matt Norlander.\n He is eligible to do so because of the extra season granted due to the COVID-19 pandemic. That report comes after Seth Trimble announced earlier in the day that he would be returning to North Carolina after previously having entered the transfer portal. \n While the best player in the conference deciding to go the professional route wouldn't have been a surprise on paper, there was plenty of uncertainty surrounding Davis' eventual decision. \n Davis is 22 years old, which may be a concern among NBA teams when directly comparing him to top prospects who are younger. Size is also a potential issue, as he is listed at 6'0 and 180 pounds. \n Perhaps he can overcome some of those factors with an eye on the 2025 draft by putting more excellent basketball on tape during his final season at North Carolina.",
    author_id=ambassador.id,
    organization_id=None,
    state="published",
    slug="slug13",
    image_url="https://www.newsobserver.com/latest-news/fdzcqv/picture285502472/alternates/LANDSCAPE_1140/RJUCONN-SP-120623-RTW.jpg",
    time=date_maker(days_in_future=-1, hour=17, minutes=4),
    modification_date=date_maker(days_in_future=-1, hour=17, minutes=4),
    synopsis="The ACC Player of the Year is reportedly coming back to North Carolina."
)

utaApp = NewsPostEntity(
    id=14,
    headline="UTA Applications are Open for Fall 2024",
    main_story="Folks, \n UTA Applications are open for Fall '24 and due May 10th. We are moving away from an AirTable form submission to a custom web application form thanks to the work of Aziz Al-Shayef and Ben Goulet. \n Applying is easy: \n 1. Login to csxl.unc.eduhttps://csxl.unc.edu/ via your ONYEN \n 2. After logging in, navigate to Academics \n 3. Look for the Become a TA! pane and complete your application \n As we transition to this new system, we ask all current UTAs applying to UTA again in the Fall to go ahead and submit this application. Please cite your current/former UTA experience in the question of 'What experience do you have providing service directly to other people?' After this cycle, we will have a different form for returners; this is our bootstrapping semester. \n One big, new feature of this application system is you can return to your application and edit it after you have submitted it. \n Thanks! \n Kris Jordan",    
    author_id=root.id,
    organization_id=None,
    state="published",
    slug="slug14",
    image_url=None,
    time=date_maker(days_in_future=-1, hour=20, minutes=16),
    modification_date=date_maker(days_in_future=-1, hour=20, minutes=16),
    synopsis="UTA Applications are open for Fall '24 and due May 10th."
)

draft = NewsPostEntity(
    id=15,
    headline="Draft Post",
    main_story="Drafted main story",    
    author_id=root.id,
    organization_id=None,
    state="draft",
    slug="slug15",
    image_url=None,
    time=date_maker(days_in_future=-1, hour=20, minutes=16),
    modification_date=date_maker(days_in_future=-1, hour=20, minutes=16),
    synopsis="Example of a Draft Post"
)

bitApp = NewsPostEntity(
    id=16,
    headline="Black in Tech Exec Applications!",
    main_story="Hello All, \n Black in Technology (BiT) is a CS Department- sponsored student organization that aims to increase community and opportunities for Black students pursuing tech careers at UNC. They are the student group also responsible for hosting AfroPix, an annual symposium that brings together Black students in tech from across the state to celebrate Black and Brown students in tech. \n Black in Tech is currently reviewing applications to be a part of BiT Executive Team and invites you to apply! This is a great opportunity to get involved in the CS community, develop relationships with other Black students in CS, and grow leadership skills along the way! \n Applications will close April 17th! Click here to access the application and learn more about each position! Please plan to spend at least 15 minutes on your application. ",    
    author_id=ambassador.id,
    organization_id=bit.id,
    state="published",
    slug="slug16",
    image_url=None,
    time=date_maker(days_in_future=-13, hour=14, minutes=28),
    modification_date=date_maker(days_in_future=-13, hour=14, minutes=28),
    synopsis="BiT Executive Team invites you to apply!"
)

comp311 = NewsPostEntity(
    id=17,
    headline="COMP 311 in Copenhagen, Denmark",
    main_story="Hello Everyone! \n I will be teaching COMP311 in Copenhagen, Denmark from May 21 - June 25, 2024! \n In addition to learning computer organization, students will be immersed in the local culture through engagement opportunities organized by our partners at DIS (https://disabroad.org/dis/) where they will gain academic knowledge and intercultural skills to prepare for a globalized world. \n You can find more information and apply for the program here: https://heelsabroad.unc.edu/index.cfm?FuseAction=Programs.ViewProgramAngular&id=11776. \n Please reach out if you have any questions! \n Best, \n Cece McMahon",    
    author_id=root.id,
    organization_id=bit.id,
    state="published",
    slug="slug17",
    image_url=None,
    time=date_maker(days_in_future=-15, hour=12, minutes=43),
    modification_date=date_maker(days_in_future=-15, hour=12, minutes=43),
    synopsis="Study abroad from May 21 - June 25, 2024!"
)





posts = [jaysonsPost, treysPost, ishmaelsPost, embreysPost, comp290, dth, nlp, cOne, fidHack, csSg, aIapp, pearlApp, utaApp, rjDavis, draft, bitApp, comp311]


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