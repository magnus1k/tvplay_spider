# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import uuid
import time
import re
from config import load_config, save_config
from collections import OrderedDict
import datetime
import os
import time


config_name = "zimuzu.conf"


def sign(account, password):
    print('Signing...')
    client_id = str(uuid.uuid1())
    headers = {'Accept': ' application/json, text/javascript, */*; q=0.01',
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
    res_headers = requests.get('http://www.zimuzu.tv/user/login', headers=headers).headers
    session = res_headers['set-cookie'][10:36]
    headers['Cookie'] = 'PHPSESSID='+session+'; CNZZDATA1254180690=784053439-1449042469-%7C1449047872'
    data = {'account': account,
            'password': password,
            'remember': '1',
            'url_back': 'http://www.zimuzu.tv/user/sign'}
    res = requests.post('http://www.zimuzu.tv/User/Login/ajaxLogin', data=data, headers=headers)
    cookie = res.headers['set-cookie']
    cookie = cookie.replace('GINFO=deleted;', '').replace('GKEY=deleted;', '')
    GINFO = re.search('GINFO=uid[^;]+', cookie).group(0)+";"
    GKEY = re.search('GKEY=[^;]+', cookie).group(0)+";"
    CPS = 'yhd%2F'+str(int(time.time()))+";"
    Cookie = ' PHPSESSID='+session+'; '+CPS+(GINFO+GKEY)*3
    headers['Cookie'] = Cookie

    playlist = load_config(config_name)
    for play in playlist:
        alluri = ""
        seasons = dict()
        res = requests.get(play["url"], headers=headers)
        # print(res.content)
        soup = BeautifulSoup(res.content, 'html.parser')

        for one in soup.find_all('li', format='HR-HDTV'):
            season = int(one['season'])
            episode = int(one['episode'])
            if (season == play['season'] and episode > play['episode']) or \
                    (season > play['season'] and episode != 0):
                link = one.find('a', href=re.compile('ed2k:'))
                uri = str(link['href'])
                if season not in seasons:
                    seasons[season] = dict()
                seasons[season][episode] = uri
        print("Got all episodes of {}".format(play['name']))
        seasons = OrderedDict(sorted(seasons.items()))

        for season in seasons:
            seasons[season] = OrderedDict(sorted(seasons[season].items()))

        for season in seasons:
            for episode in seasons[season]:
                uri = seasons[season][episode]
                alluri += uri + "\n\r"
                play['season'] = season
                play['episode'] = episode

        timenow = datetime.datetime.now().strftime("%Y-%m-%d")
        if not os.path.exists("zimuzu_txt"):
            os.makedirs("zimuzu_txt")
        filename = os.path.join("zimuzu_txt", "zimuzu_{}.txt".format(timenow))
        print(filename)
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(alluri)
            save_config(playlist, config_name)

        time.sleep(10)
