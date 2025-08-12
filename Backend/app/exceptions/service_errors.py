class EmailAlreadyExistsException(Exception):
    pass

class ServerErrorException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

class UserAlreadyVerifiedException(Exception):
    pass

class InvalidVerificationTokenException(Exception):
    pass

class FacultyDoesNotBelongToUniversityException(Exception):
    pass

class MajorDoesNotBelongToFacultyException(Exception):
    pass

class InvalidInputException(Exception):
    pass

class MajorRequiresFacultyException(Exception): 
    pass

class InvalidCredentialsException(Exception):
    pass

class UserNotVerifiedException(Exception):
    pass

class GroupNotFoundException(Exception):
    pass

class GroupNotBelongToUniversityException(Exception):
    pass

class InvalidGroupPasswordException(Exception):
    pass


class InvalidVerificationTokenException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

class AlreadyHasRoleException(Exception):
    pass

class FacultyDoesNotBelongToUniversityException(Exception):
    pass

class MajorDoesNotBelongToFacultyException(Exception):
    pass    