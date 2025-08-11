class EmailAlreadyExistsException(Exception):
    pass

class ServerErrorException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

class UserAlreadyVerifiedException(Exception):
    pass