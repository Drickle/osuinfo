# Exceptions.py for osuinfo 
# Represents some exceptions that everything used
from .Logger import logger

class InvalidAPIKey(BaseException):
    def __init__(self,arg=''):
        logger.error(f"Bad API Key {arg}.")
        return

class CantAccessAPI(BaseException):
    def __init__(self):
        logger.error(f'Unable to reach osu!API. Needs attention!')
        return

class NosuchUser(BaseException):
    def __init__(self,user):
        self.user = user
        logger.error(f'The user {user} appears to be a invalid user.')
        return

class NoRecentException(BaseException):
    def __init__(self,user, origin):
        self.user = user
        self.origin = origin.__str__()
        logger.error(f"The user {user} appears to be inactive recently. \n{origin}")

    def __str__(self):
        return f"The user {user} appears to be inactive recently. \n{origin}"

