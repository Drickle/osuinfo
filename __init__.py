from .User import User as __User
from .Exceptions import *
from .Logger import logger
apikey = None
GetFromWebPage = False

def set_key(key,Check=True):
    if Check:
        logger.info("Testing API key...")
        import urllib.error
        from urllib import request
        try:
            respond = request.urlopen(f"https://osu.ppy.sh/api/get_user?k={key}&u=peppy")
        except urllib.error.HTTPError:
            raise InvalidAPIKey(key)
        logger.info("API Key check success!")
    global apikey
    apikey = key

def EnableWebPage(toggle):
    global GetFromWebPage
    GetFromWebPage = bool(toggle)

def NewUser(user,mode='osu',isID=False,Decimal='dot'):
    if mode == None: mode = 'osu'
    try:
        return __User(user,apikey,mode=mode,isID=False,GetFromWebPage=GetFromWebPage,Decimal=Decimal)
    except NosuchUser as e:
        raise NosuchUser(e.user)