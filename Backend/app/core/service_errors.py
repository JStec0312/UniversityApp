from http import HTTPStatus

class AppError(Exception):
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    code: str = "INTERNAL_ERROR"
    message: str = "Internal server error."
    headers: dict | None = None
    extra: dict

    def __init__(self, message: str | None = None, *,
                 code: str | None = None,
                 headers: dict | None = None,
                 extra: dict | None = None):
        super().__init__(message or self.message)
        if message: self.message = message
        if code: self.code = code
        self.headers = headers
        self.extra = extra or {}

# 4xx/5xx domenowe — zachowujemy Twoje nazwy

class EmailAlreadyExistsException(AppError):
    status_code = HTTPStatus.CONFLICT
    code = "EMAIL_ALREADY_EXISTS"
    message = "Email already exists."

class ServerErrorException(AppError):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    code = "INTERNAL_ERROR"
    message = "Internal server error."

class UserNotFoundException(AppError):
    status_code = HTTPStatus.NOT_FOUND
    code = "USER_NOT_FOUND"
    message = "User not found."

class UserAlreadyVerifiedException(AppError):
    status_code = HTTPStatus.CONFLICT
    code = "USER_ALREADY_VERIFIED"
    message = "User already verified."

class InvalidVerificationTokenException(AppError):
    status_code = HTTPStatus.BAD_REQUEST  # to nie jest token auth -> 400
    code = "INVALID_VERIFICATION_TOKEN"
    message = "Invalid verification token."

class FacultyDoesNotBelongToUniversityException(AppError):
    status_code = HTTPStatus.BAD_REQUEST
    code = "FACULTY_NOT_IN_UNIVERSITY"
    message = "Faculty does not belong to specified university."

class MajorDoesNotBelongToFacultyException(AppError):
    status_code = HTTPStatus.BAD_REQUEST
    code = "MAJOR_NOT_IN_FACULTY"
    message = "Major does not belong to specified faculty."

class InvalidInputException(AppError):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    code = "VALIDATION_ERROR"
    message = "The request failed validation."

class MajorRequiresFacultyException(AppError):
    status_code = HTTPStatus.BAD_REQUEST
    code = "MAJOR_REQUIRES_FACULTY"
    message = "Selecting a major requires selecting a faculty."

class InvalidCredentialsException(AppError):
    status_code = HTTPStatus.UNAUTHORIZED
    code = "INVALID_CREDENTIALS"
    message = "Invalid credentials."

class UserNotVerifiedException(AppError):
    status_code = HTTPStatus.FORBIDDEN
    code = "USER_NOT_VERIFIED"
    message = "User not verified."

class GroupNotFoundException(AppError):
    status_code = HTTPStatus.NOT_FOUND
    code = "GROUP_NOT_FOUND"
    message = "Group not found."

class GroupNotBelongToUniversityException(AppError):  # zachowuję Twoją nazwę
    status_code = HTTPStatus.BAD_REQUEST
    code = "GROUP_NOT_IN_UNIVERSITY"
    message = "Group does not belong to specified university."

class InvalidGroupPasswordException(AppError):
    status_code = HTTPStatus.FORBIDDEN  # logika dostępowa -> 403
    code = "INVALID_GROUP_PASSWORD"
    message = "Invalid group password."

class AlreadyHasRoleException(AppError):
    status_code = HTTPStatus.CONFLICT
    code = "ALREADY_HAS_ROLE"
    message = "User already has this role."

class GroupAlreadyExistsException(AppError):
    status_code = HTTPStatus.CONFLICT
    code = "GROUP_ALREADY_EXISTS"
    message = "Group already exists."

class GroupHasDependenciesException(AppError):
    status_code = HTTPStatus.CONFLICT
    code = "GROUP_HAS_DEPENDENCIES"
    message = "Group has dependent resources and cannot be modified."
    
class NoPermissionForInvitationException(AppError):
    status_code = HTTPStatus.FORBIDDEN
    code = "NO_PERMISSION_FOR_INVITATION"
    message = "User does not have permission to invite others to this group."

class UserAlreadyInGroupException(AppError):
    status_code = HTTPStatus.CONFLICT
    code = "USER_ALREADY_IN_GROUP"
    message = "User is already a member of this group."

class NotPermittedForThisInvitationException(AppError):
    status_code = HTTPStatus.FORBIDDEN
    code = "NOT_PERMITTED_FOR_THIS_INVITATION"
    message = "User is not permitted to accept this invitation."

class InvitationNotFoundException(AppError):
    status_code = HTTPStatus.NOT_FOUND
    code = "INVITATION_NOT_FOUND"
    message = "Invitation not found."

class InvitationNotActiveException(AppError):
    status_code = HTTPStatus.BAD_REQUEST
    code = "INVITATION_NOT_ACTIVE"
    message = "Invitation is not active."

InvalidVerificationToken = InvalidVerificationTokenException
UserNotFound = UserNotFoundException
EmailAlreadyExists = EmailAlreadyExistsException
GroupNotInUniversityException = GroupNotBelongToUniversityException  # lepsza nazwa, alias zostawiony

__all__ = [
    "AppError",
    "EmailAlreadyExistsException",
    "ServerErrorException",
    "UserNotFoundException",
    "UserAlreadyVerifiedException",
    "InvalidVerificationTokenException",
    "FacultyDoesNotBelongToUniversityException",
    "MajorDoesNotBelongToFacultyException",
    "InvalidInputException",
    "MajorRequiresFacultyException",
    "InvalidCredentialsException",
    "UserNotVerifiedException",
    "GroupNotFoundException",
    "GroupNotBelongToUniversityException",
    "InvalidGroupPasswordException",
    "AlreadyHasRoleException",
    "GroupAlreadyExistsException",
    "GroupHasDependenciesException",
    # aliasy
    "InvalidVerificationToken",
    "UserNotFound",
    "EmailAlreadyExists",
    "GroupNotInUniversityException",
    "NoPermissionForInvitationException",
    "UserAlreadyInGroupException",
    "NotPermittedForThisInvitationException",
    "InvitationNotFoundException",
    "InvitationNotActiveException"
]

class UserAlreadyInvitedError(AppError):
    status_code = HTTPStatus.CONFLICT
    code = "USER_ALREADY_INVITED"
    message = "User is already invited to this group."
