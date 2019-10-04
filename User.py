# User.py for osuinfo 
# Represents user related things.
# Copyright Cinhi Young. Licensed under MIT.
from .Constants import (
    apihead,webhead,getuser,flags
)
from .Exceptions import *
from .Logger import logger
from urllib import request
import json

def formatDec(data,decimal='dot'):
    return '{0:.2f}'.format(data) if decimal == 'dot' else ('{0:.2f}'.format(data)).replace('.',',')

def formatPct(data,decimal='dot'):
    return '{0:.2%}'.format(data) if decimal == 'dot' else ('{0:.2%}'.format(data)).replace('.',',')

def formatSep(data,decimal='dot'):
    return '{:,}'.format(data) if decimal == 'dot' else ('{:,}'.format(data)).replace(',','.')

def Parse_rawjson(source,fromwhat,type,mode=''):
    if type == 'info':
        tmpdict = {
            'id'            :   int((source['id']                   if fromwhat == 0 else source['user_id'])),
            'username'      :   source['username'],
            'country'       :   source['country']['code'],
            'avatar'        :   str(source['avatar_url']            if fromwhat == 0 else None),
            'cover'         :   str(source['cover_url']             if fromwhat == 0 else None),
            'issupporter'   :   str(source['is_supporter']          if fromwhat == 0 else None),
            'mode'          :   str(mode)
        }
        return tmpdict
    else :
        tmpdict = {
            'level'         : int(source['level']['current']          if fromwhat == 0 else int(source['level'])),
            'lvprgs'        : float(source['level']['progress'] / 100 if fromwhat == 0 else float(source['level']\
                            - int(source['level']))),
            'rank'          : int(source['pp_rank']),
            'countryrank'   : int(source['rank']['country']         if fromwhat == 0 else source['pp_country_rank']),
            'totalplaytime' : int(source['play_time']               if fromwhat == 0 else source['total_seconds_played']),
            'playcount'     : int(source['play_count']              if fromwhat == 0 else source['playcount']),
            'accuracy'      : float(source['hit_accuracy']            if fromwhat == 0 else source['accuracy']),
            'rankedscore'   : int(source['ranked_score']),
            'totalhits'     : int(source['total_hits']              if fromwhat == 0 else (source['count300'] + \
                                                                    source['count1000'] + source['count50'])),
            'totalscore'    : int(source['total_score']),
            'maxcombo'      : int(source['maximum_combo']           if fromwhat == 0 else None),
            'pp'            : float(source['pp']                    if fromwhat == 0 else source['pp_raw']),
            'rankcounts'    : {
                'ssh'       : int(source['grade_counts']['ssh']     if fromwhat == 0 else source['count_rank_ssh']),
                'ss'        : int(source['grade_counts']['ss']      if fromwhat == 0 else source['count_rank_ss']),
                'sh'        : int(source['grade_counts']['sh']      if fromwhat == 0 else source['count_rank_sh']),
                's'         : int(source['grade_counts']['s']       if fromwhat == 0 else source['count_rank_s']),
                'a'         : int(source['grade_counts']['a']       if fromwhat == 0 else source['count_rank_a'])
            }
        }
        return tmpdict


class Info:
    '''
    Represents basic information of the user.
    Since there's no `struct` in Python, we created a classified data structre lol
    '''
    def __init__(self,dict):
        self.id             = dict['id']            # int
        self.username       = dict['username']      # str
        self.country        = dict['country']       # str
        self.countryflag    = flags[dict['country']] if flags.get(dict['country'],'') != "" else ''     # str
        self.avatar         = dict['avatar']        # str of avatar link    
        self.cover          = dict['cover']         # str or None
        self.issupporter    = dict['issupporter']   # bool or None
        self.profile        = f'https://osu.ppy.sh/users/{self.id}/{dict["mode"]}'

class Statistics:
    '''
    Same as above `struct` -like data structre.
    '''
    def __init__(self,dict,Decimal):
        self.level          = dict['level']                                                 # int
        self.lvprogress     = dict['lvprgs']                                                # float
        self.lvprogressf    = formatPct(self.lvprogress,decimal=Decimal)
        self.rank           = dict['rank']                                                  # int
        self.rankf          = formatSep(self.rank,Decimal)                                  # str
        self.countryrank    = dict['countryrank']                                           # int
        self.countryrankf   = formatSep(dict['countryrank'],Decimal)                        # str
        self.totalplaytime  = dict['totalplaytime']                                         # int
        self.totalplaytimef = '{:02}h {:02}m {:02}s'.format(self.totalplaytime//3600,\
                              self.totalplaytime%3600//60, self.totalplaytime%60)           # str
        self.playcount      = dict['playcount']                                             # int
        self.playcountf     = formatSep(self.playcount,Decimal)                             # str
        self.accuracy       = dict['accuracy']                                              # float
        self.accuracyf      = formatDec(self.accuracy,Decimal)                              # str
        self.rankedscore    = dict['rankedscore']                                           # int
        self.rankedscoref   = formatSep(self.rankedscore,Decimal)                           # str
        self.totalhits      = dict['totalhits']                                             # int
        self.totalhitsf     = formatSep(self.totalhits,Decimal)                             # str
        self.totalscore     = dict['totalscore']                                            # int
        self.totalscoref    = formatSep(self.totalscore,Decimal)                            # str
        self.maxcombo       = dict['maxcombo']                                              # int
        self.maxcombof      = formatSep(self.maxcombo,Decimal)                              # str
        self.pp             = dict['pp']                                                    # int
        self.pp_f           = formatDec(self.pp,Decimal)                                    # str
        self.rankcounts     = (dict['rankcounts']['ssh'],   dict['rankcounts']['ss'],   dict['rankcounts']['sh'],\
                               dict['rankcounts']['s'],     dict['rankcounts']['a'])        # tuple(int,int,...)

class User:
    def __init__(self,user,apikey,
                 mode="osu",isID=False,GetFromWebPage=False,
                 Decimal='dot'):
        # print(f"Successfully initialized user {user} with API key {apikey}.")
        logger.info(f"Acquiring info of {user}...")
        WebSuccess = False
        if GetFromWebPage:
            self.mode = mode.replace('ctb','fruits')
            logger.info("Getting data from " + (f"{webhead}users/{user}/{self.mode}"))
            try:
                
                self.rawjson = json.loads(request.urlopen(f"{webhead}users/{user}/{self.mode}").read().decode('utf-8')\
                    .partition('  <script id="json-user" type="application/json">')[2]\
                    .partition('</script>')[0])                                 # < --- Cut the string with the content we need.
                WebSuccess = True                                               #     | We only use the `<json-user>` element here.
                self.__source = 0                                               # < --- Identify where the data get.
            except request.HTTPError as e:
                if e.code == 404:
                    raise NosuchUser(user)
                else:
                    logger.error("Unable to get data from web page, acquiring from osu!API.")
            except request.URLError:                                            #     | 0 = WebPage, 1 = osu!API
                raise CantAccessAPI
           
            except:
                logger.error("Unable to get data from web page, acquiring from osu!API.")
        if WebSuccess != True:
            print("osu!API is hiring!")
            try:
                self.rawjson = json.loads(request.urlopen(f"{apihead}{getuser}{apikey}&u={user}")\
                            .read().decode('utf-8'))[0]
                print("osu!API hired.")
            except request.HTTPError as e:
                if e.code == 404:
                    raise NosuchUser(user)
                if e.code == 401:
                    raise CantAccessAPI
            except request.URLError:
                raise CantAccessAPI
        self.info = Info(dict=(Parse_rawjson(self.rawjson,self.__source,mode=mode,type='info')))
        self.stat = Statistics(dict=Parse_rawjson((self.rawjson['statistics'] if self.__source == 0 else self.rawjson),self.__source,type='statistics'),Decimal=Decimal)
