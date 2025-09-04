from http import HTTPStatus

class AppError(Exception):
    """Base exception class for application errors."""
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
        if message:
            self.message = message
        if code:
            self.code = code
        self.headers = headers
        self.extra = extra or {}

# --- Main exception categories ---

class NotFoundError(AppError):
    """Base class for all 'not found' errors."""
    status_code = HTTPStatus.NOT_FOUND
    code = "RESOURCE_NOT_FOUND"
    message = "The requested resource was not found."

class ForbiddenError(AppError):
    """Base class for all permission and authorization errors."""
    status_code = HTTPStatus.FORBIDDEN
    code = "FORBIDDEN"
    message = "You don't have permission to perform this action."

class ConflictError(AppError):
    """Base class for all conflicts with current state."""
    status_code = HTTPStatus.CONFLICT
    code = "CONFLICT"
    message = "This operation conflicts with the current state."

class ValidationError(AppError):
    """Base class for validation errors."""
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    code = "VALIDATION_ERROR"
    message = "The request failed validation."

class BadRequestError(AppError):
    """Base class for malformed or invalid requests."""
    status_code = HTTPStatus.BAD_REQUEST
    code = "BAD_REQUEST"
    message = "The request is invalid."

class UnauthorizedError(AppError):
    """Base class for authentication failures."""
    status_code = HTTPStatus.UNAUTHORIZED
    code = "UNAUTHORIZED"
    message = "Authentication is required."

class ServerError(AppError):
    """Base class for server-side errors."""
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    code = "INTERNAL_ERROR"
    message = "Internal server error."

# --- Resource-specific not found errors ---

class UserNotFoundError(NotFoundError):
    code = "USER_NOT_FOUND"
    message = "User not found."

class GroupNotFoundError(NotFoundError):
    code = "GROUP_NOT_FOUND"
    message = "Group not found."

class InvitationNotFoundError(NotFoundError):
    code = "INVITATION_NOT_FOUND"
    message = "Invitation not found."

# --- Resource-specific conflict errors ---

class EmailAlreadyExistsError(ConflictError):
    code = "EMAIL_ALREADY_EXISTS"
    message = "Email already exists."

class UserAlreadyVerifiedError(ConflictError):
    code = "USER_ALREADY_VERIFIED"
    message = "User already verified."

class UserAlreadyInGroupError(ConflictError):
    code = "USER_ALREADY_IN_GROUP"
    message = "User is already a member of this group."

class GroupAlreadyExistsError(ConflictError):
    code = "GROUP_ALREADY_EXISTS"
    message = "Group already exists."

class GroupHasDependenciesError(ConflictError):
    code = "GROUP_HAS_DEPENDENCIES"
    message = "Group has dependent resources and cannot be modified."

class UserIsAlreadyAdminError(ConflictError):
    code = "USER_IS_ALREADY_ADMIN"
    message = "User is already an admin of this group."

class AlreadyHasRoleError(ConflictError):
    code = "ALREADY_HAS_ROLE"
    message = "User already has this role."

class UserAlreadyInvitedError(ConflictError):
    code = "USER_ALREADY_INVITED"
    message = "User is already invited to this group."

# --- Permission/authorization errors ---

class PermissionError(ForbiddenError):
    """Base class for permission errors."""
    code = "PERMISSION_DENIED"
    message = "You don't have permission to perform this action."

class InvitationPermissionError(PermissionError):
    code = "NO_PERMISSION_FOR_INVITATION"
    message = "User does not have permission to invite others to this group."

class InvitationAccessError(PermissionError):
    code = "NOT_PERMITTED_FOR_THIS_INVITATION" 
    message = "User is not permitted to access this invitation."

class AdminPermissionError(PermissionError):
    code = "NO_PERMISSION_FOR_ADMIN_ACTION"
    message = "User does not have permission to perform admin actions."

class UserNotMemberError(PermissionError):
    code = "USER_IS_NOT_MEMBER"
    message = "User is not a member of this group."

class UserNotVerifiedError(ForbiddenError):
    code = "USER_NOT_VERIFIED"
    message = "User not verified."

# --- Validation and business rule errors ---

class RelationshipError(BadRequestError):
    """Base class for relationship constraint violations."""
    code = "RELATIONSHIP_ERROR"
    message = "Entity relationship constraint violated."

class FacultyNotInUniversityError(RelationshipError):
    code = "FACULTY_NOT_IN_UNIVERSITY"
    message = "Faculty does not belong to specified university."

class MajorNotInFacultyError(RelationshipError):
    code = "MAJOR_NOT_IN_FACULTY"
    message = "Major does not belong to specified faculty."

class GroupNotInUniversityError(RelationshipError):
    code = "GROUP_NOT_IN_UNIVERSITY"
    message = "Group does not belong to specified university."

class MajorRequiresFacultyError(BadRequestError):
    code = "MAJOR_REQUIRES_FACULTY"
    message = "Selecting a major requires selecting a faculty."

class InvalidVerificationTokenError(BadRequestError):
    code = "INVALID_VERIFICATION_TOKEN"
    message = "Invalid verification token."

class InvitationNotActiveError(BadRequestError):
    code = "INVITATION_NOT_ACTIVE"
    message = "Invitation is not active."

class InvalidGroupPasswordError(UnauthorizedError):
    code = "INVALID_GROUP_PASSWORD"
    message = "Invalid group password."

class InvalidCredentialsError(UnauthorizedError):
    code = "INVALID_CREDENTIALS"
    message = "Invalid credentials."

# --- Legacy aliases (for backward compatibility) ---
# All these will reference the new error classes for compatibility
EmailAlreadyExistsException = EmailAlreadyExistsError
ServerErrorException = ServerError
UserNotFoundException = UserNotFoundError
UserAlreadyVerifiedException = UserAlreadyVerifiedError
InvalidVerificationTokenException = InvalidVerificationTokenError
FacultyDoesNotBelongToUniversityException = FacultyNotInUniversityError
MajorDoesNotBelongToFacultyException = MajorNotInFacultyError
InvalidInputException = ValidationError
MajorRequiresFacultyException = MajorRequiresFacultyError
InvalidCredentialsException = InvalidCredentialsError
UserNotVerifiedException = UserNotVerifiedError
GroupNotFoundException = GroupNotFoundError
GroupNotBelongToUniversityException = GroupNotInUniversityError
InvalidGroupPasswordException = InvalidGroupPasswordError
AlreadyHasRoleException = AlreadyHasRoleError
GroupAlreadyExistsException = GroupAlreadyExistsError
GroupHasDependenciesException = GroupHasDependenciesError
NoPermissionForInvitationException = InvitationPermissionError
UserAlreadyInGroupException = UserAlreadyInGroupError
NotPermittedForThisInvitationException = InvitationAccessError
InvitationNotFoundException = InvitationNotFoundError
InvitationNotActiveException = InvitationNotActiveError
NoPermissionForMakingAdminException = AdminPermissionError
UserIsNotMemberOfGroupException = UserNotMemberError
UserIsAlreadyAdminException = UserIsAlreadyAdminError
ForbiddenToSeeInvitationsException = PermissionError
ForbiddenToCancelInvitationException = PermissionError

# Other common aliases
InvalidVerificationToken = InvalidVerificationTokenError
UserNotFound = UserNotFoundError
EmailAlreadyExists = EmailAlreadyExistsError
GroupNotInUniversityException = GroupNotInUniversityError

__all__ = [
    # Base classes
    "AppError",
    "NotFoundError",
    "ForbiddenError",
    "ConflictError",
    "ValidationError",
    "BadRequestError",
    "UnauthorizedError",
    "ServerError",
    "PermissionError",
    "RelationshipError",
    
    # Not Found errors
    "UserNotFoundError",
    "GroupNotFoundError",
    "InvitationNotFoundError",
    
    # Conflict errors
    "EmailAlreadyExistsError",
    "UserAlreadyVerifiedError",
    "UserAlreadyInGroupError",
    "GroupAlreadyExistsError", 
    "GroupHasDependenciesError",
    "UserIsAlreadyAdminError",
    "AlreadyHasRoleError",
    "UserAlreadyInvitedError",
    
    # Permission errors
    "InvitationPermissionError",
    "InvitationAccessError", 
    "AdminPermissionError",
    "UserNotMemberError",
    "UserNotVerifiedError",
    
    # Validation errors
    "FacultyNotInUniversityError",
    "MajorNotInFacultyError",
    "GroupNotInUniversityError",
    "MajorRequiresFacultyError",
    "InvalidVerificationTokenError",
    "InvitationNotActiveError",
    
    # Auth errors
    "InvalidGroupPasswordError",
    "InvalidCredentialsError",
    
    # Legacy exceptions (for backward compatibility)
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
    "NoPermissionForInvitationException",
    "UserAlreadyInGroupException",
    "NotPermittedForThisInvitationException",
    "InvitationNotFoundException",
    "InvitationNotActiveException", 
    "NoPermissionForMakingAdminException",
    "UserIsNotMemberOfGroupException",
    "UserIsAlreadyAdminException",
    "ForbiddenToSeeInvitationsException",
    "ForbiddenToCancelInvitationException",
    
    # Common aliases
    "InvalidVerificationToken",
    "UserNotFound",
    "EmailAlreadyExists",
    "GroupNotInUniversityException",
]
