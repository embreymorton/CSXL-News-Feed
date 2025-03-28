"""Package for all models in the application."""

from .application import (
    Application,
    UTAApplication,
    NewUTAApplication,
    ReturningUTAApplication,
)
from .application_details import (
    ApplicationDetails,
    UTAApplicationDetails,
    NewUTAApplicationDetails,
    ReturningUTAApplicationDetails,
)
from .pagination import Paginated, PaginationParams, EventPaginationParams
from .permission import Permission
from .user import User, ProfileForm
from .user_details import UserDetails
from .unregistered_user import UnregisteredUser
from .role import Role
from .role_details import RoleDetails
from .organization import Organization
from .event import Event
from .public_user import PublicUser
from .event_details import EventDetails
from .room import Room
from .room_details import RoomDetails
from .event_registration import (
    EventRegistration,
    NewEventRegistration,
)
from .registration_type import RegistrationType
from .news_post import NewsPost
from .news_post_details import NewsPostDetails

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"
