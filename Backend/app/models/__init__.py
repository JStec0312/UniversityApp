from app.models.base import BaseModel
from app.models.user import User
from app.models.student import Student
from app.models.admin import Admin
from app.models.news import News
from app.models.event import Event
from app.models.event_rsvp import EventRSVP
from app.models.discount import Discount
from app.models.forum_post import ForumPost
from app.models.university import University
from app.models.faculty import Faculty
from app.models.major import Major
from app.models.group import Group
from app.models.superior_group import SuperiorGroup
from app.models.superior_admins import SuperiorAdmin

# This allows importing all models from the models package like:
# from app.models import User, Student, etc.