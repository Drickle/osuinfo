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


