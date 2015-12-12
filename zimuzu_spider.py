# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import uuid
import re
from config import load_config, save_config
import time
from misc import get_url, sort_plays, save_uri


class ZimuzuSite:
    def __init__(self, filename=""):
        self.headers = dict()
        self.account = ""
        self.password = ""
        if filename != "":
            account_file = load_config(filename)
            self.account = account_file['account']
            self.password = account_file['password']

    def __sign(self, account, password):
        print('Signing...')
        client_id = str(uuid.uuid1())
        self.headers = {'Accept': ' application/json, text/javascript, */*; q=0.01',
                        'X-DevTools-Emulate-Network-Conditions-Client-Id': client_id,
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-FirePHP-Version': '0.0.6',
                        'Host': 'www.zimuzu.tv',
                        'Origin': 'http://www.zimuzu.tv',
                        'Referer': 'http://www.zimuzu.tv/user/login',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/42.0.2311.90 Safari/537.36',
                        'Accept-Encoding': ' gzip, deflate, sdch',
                        'Accept-Language': ' zh-CN,zh;q=0.8'}
        res_headers = requests.get('http://www.zimuzu.tv/user/login', headers=self.headers).headers
        session = res_headers['set-cookie'][10:36]
        self.headers['Cookie'] = 'PHPSESSID='+session+'; CNZZDATA1254180690=784053439-1449042469-%7C1449047872'
        data = {'account': account,
                'password': password,
                'remember': '1',
                'url_back': 'http://www.zimuzu.tv/user/sign'}
        res = requests.post('http://www.zimuzu.tv/User/Login/ajaxLogin', data=data, headers=self.headers)
        cookie = res.headers['set-cookie']
        cookie = cookie.replace('GINFO=deleted;', '').replace('GKEY=deleted;', '')
        GINFO = re.search('GINFO=uid[^;]+', cookie).group(0)+";"
        GKEY = re.search('GKEY=[^;]+', cookie).group(0)+";"
        CPS = 'yhd%2F'+str(int(time.time()))+";"
        Cookie = ' PHPSESSID='+session+'; '+CPS+(GINFO+GKEY)*3
        self.headers['Cookie'] = Cookie

    def __get_play_from_webpage(self, webpage, play):
        soup = BeautifulSoup(webpage, 'html.parser')
        seasons = dict()
        for one in soup.find_all('li', format='HR-HDTV'):
            season = int(one['season'])
            episode = int(one['episode'])
            if (season == play['season'] and episode > play['episode']) or \
                    (100 > season > play['season'] and episode != 0):
                link = one.find('a', href=re.compile('ed2k:'))
                uri = str(link['href'])
                if season not in seasons:
                    seasons[season] = dict()
                seasons[season][episode] = uri
        print("Got all episodes of {}".format(play['name']))
        return seasons

    def get_plays(self, config_name, user):
        if self.account != "" and self.password != "":
            self.__sign(self.account, self.password)
        playlist = load_config(config_name)
        for play in playlist:
            alluri = ""

            webpage = get_url(play["url"],self.headers)
            seasons = sort_plays(self.__get_play_from_webpage(webpage, play))

            for season in seasons:
                for episode in seasons[season]:
                    uri = seasons[season][episode]
                    alluri += uri + "\n\r"
                    play['season'] = season
                    play['episode'] = episode

            save_uri("zimuzu", alluri, user)
            save_config(playlist, config_name)

            time.sleep(10)

