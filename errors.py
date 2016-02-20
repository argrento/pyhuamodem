"""Exceptions and error-handling methods."""

ERROR_CODES = ['100002', '100003', '100004', '108001', '108002', '108003',
               '108006', '108007', '120001', '125001', '125002', '125003']


class ErrorSystemNotSupport(Exception):
    """
    System not supported error -- 100002
    """
    pass

    
class ErrorSystemNoRights(Exception):
    """
    System has no rights error -- 100003
    """
    pass

    
class ErrorSystemBusy(Exception):
    """
    System is busy error -- 100004
    """
    pass


class ErrorLoginUsernameWrong(Exception):
    """
    Wrong username error -- 108001
    """
    pass

    
class ErrorLoginPasswordWrong(Exception):
    """
    Wrong password error -- 108002
    """
    pass

    
class ErrorUserAlreadyLogin(Exception):
    """
    User is logged in error -- 108003
    """
    pass

    
class ErrorLoginUsernamePwdWrong(Exception):
    """
    Wrong username and password --- 108006
    """
    pass

    
class ErrorLoginUsernamePwdOverrun(Exception):
    """
    Wrong username and password --- 108007
    """
    pass

    
class ErrorVoiceBusy(Exception):
    """
    Voice busy error -- 120001
    """
    pass


class ErrorWrongToken(Exception):
    """
    Wrong token error -- 125001
    """
    pass


class ErrorWrongSession(Exception):
    """
    Wrong session error -- 125002
    """
    pass


class ErrorWrongSessionToken(Exception):
    """
    Wrong session token error -- 125003
    """
    pass


class ErrorUnknownError(Exception):
    """
    Any other unknown error
    """
    pass
