# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import uuid
import time
import re
# import xmlrpc.client
import subprocess
from config import load_config
import os


config_name = "zimuzu.conf"


def sign(account, password):
    print('signing...')
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
    print(res_headers)
    session = res_headers['set-cookie'][10:36]
    print(session)
    headers['Cookie'] = 'PHPSESSID='+session+'; CNZZDATA1254180690=784053439-1449042469-%7C1449047872'
    data = {'account': account,
            'password': password,
            'remember': '1',
            'url_back': 'http://www.zimuzu.tv/user/sign'}
    res = requests.post('http://www.zimuzu.tv/User/Login/ajaxLogin', data=data, headers=headers)
    print(res.headers)
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

    for play in playlist:

        res = requests.get(play["url"], headers=headers)
        print(res.content)
        soup = BeautifulSoup(res.content, 'html.parser')
        alluri = ""
        for one in soup.find_all('li', format='HR-HDTV'):
            if (int(one['season']) == play['season'] and int(one['episode']) > play['episode']) or \
                    (int(one['season']) > play['season'] and int(one['episode']) != 0):
                link = one.find('a', href=re.compile('ed2k:'))
                alluri += str(link['href']) + "\n"

                # I have trouble to download magnet with aria2, I will try something else.
                # with xmlrpc.client.ServerProxy("http://localhost:6800/rpc") as proxy:
                #     val = proxy.aria2.addUri([str(link['href'])])
                #     print(val)

                # Too many times access Xunlei will cause "Verification code required"
                # os.system('python2 C:\\Users\\Administrator\\Documents\\xunlei-lixian\\lixian_cli.py download --tool=a2 "{}"'.format(str(link['href'])))
                print(str(link['href']))
        # subprocess.call(["C:\Program Files (x86)\Thunder Network\Thunder\Program\Thunder.exe", alluri],
        #                 shell=True)
