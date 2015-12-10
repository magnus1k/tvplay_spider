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
    # requests.get("http://www.zimuzu.tv/user/sign", headers=headers).content
    # print('wait for 20 seconds...')
    # time.sleep(20)
    # content = requests.get("http://www.zimuzu.tv/user/sign/dosign", headers=headers).json()
    # print("sign success! ") if content['data'] != False else ("signed! " if content['data'] == False else
    #                                                           "sign failed! " + str(content)), content['status']

    playlist = load_config(config_name)
    alluri = ""
    for play in playlist:
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
                # alluri += str(link['href']) + "\n"

                # I have trouble to download magnet with aria2, I will try something else.
                # with xmlrpc.client.ServerProxy("http://localhost:6800/rpc") as proxy:
                #     val = proxy.aria2.addUri([str(link['href'])])
                #     print(val)

                # Too many times access Xunlei will cause "Verification code required"

                # os.system('python2 E:\\xunlei-lixian\\lixian_cli.py download '
                #           '--tool=aria2 --continue "{}"'.format(str(link['href'])))
        print("Got all episodes of {}".format(play['name']))
        # os.system('C:\\Python27\\python.exe E:\\xunlei-lixian\\lixian_cli.py login')
        seasons = OrderedDict(sorted(seasons.items()))
        for season in seasons:
            seasons[season] = OrderedDict(sorted(seasons[season].items()))
        for season in seasons:
            for episode in seasons[season]:
                # uri = seasons[season][episode]
                # exit_code = -1
                # retry_times = 0
                # while exit_code != 0 and retry_times < 10000:
                #     print("Start downloading {} season {} episode {}".format(play['name'], season, episode))
                #     exit_code = os.system('C:\\Python27\\python.exe E:\\xunlei-lixian\\lixian_cli.py '
                #                           'download --tool=aria2 --continue "{}"'.format(uri))
                #     # exit_code = subprocess.call(['C:\\Python27\\python.exe', 'E:\\xunlei-lixian\\lixian_cli.py',
                #     #                              'download', '--tool=aria2', '--continue', '"{}"'.format(uri)])
                #     print(exit_code)
                #     if exit_code != 0:
                #         retry_times += 1
                #         print("Something wrong. Wait one minute...")
                #         sleep(60)
                #         print("Start retry {}".format(retry_times))
                #
                #     else:
                #         print("{} season {} episode {} downloaded".format(play['name'], season, episode))
                uri = seasons[season][episode]
                alluri += uri + "\n\r"
                play['season'] = season
                play['episode'] = episode
                save_config(playlist, config_name)

    timenow = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join("zimuzu_txt", "zimuzu_{}.txt".format(timenow))
    print(filename)
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(alluri)
