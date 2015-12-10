# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from config import load_config


config_name = "dmhy.conf"


def dmhy_find_url(url, pattern, episode):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    alluri = ""
    page = 1
    findep = False

    while not findep:
        realurl = url + "/page/" + str(page)
        res = requests.get(realurl, headers)
        soup = BeautifulSoup(res.content, 'html.parser')

        lastpage = re.search("沒有可顯示資源", str(soup.text))
        if lastpage:
            break

        for tr in soup.find_all('tr'):
            for a in tr.find_all('a'):
                if a.has_attr('target') and a['target'] == '_blank':
                    match = re.search(pattern, str(a.text))
                    if match:
                        ep = int(str(match.group('ep')).strip())
                        if ep == episode:
                            findep = True
                            print("page:" + str(page))
                        elif ep > episode:
                            print("1080p:" + str(a.text).strip())
                            print("ep:" + str(ep))
                            link = tr.find('a', href=re.compile('magnet:'))
                            alluri += str(link['href']) + "\n"
                            print("link:" + link['href'])

        page += 1

    return alluri


def download():
    playlist = load_config(config_name)
    alluri = ""
    for play in playlist:
        alluri += dmhy_find_url(play["url"], play["pattern"], play["episode"])

    print("alluri:\n" + alluri)


download()


