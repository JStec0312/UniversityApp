from enum import Enum

class  RoleEnum(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"
    SUPERIOR_ADMIN = "superior_admin"