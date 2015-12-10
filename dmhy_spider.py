# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from config import load_config, save_config
from collections import OrderedDict
import datetime
import os

config_name = "dmhy.conf"


def dmhy_find_url(play):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}

    alluri = ""
    page = 1
    findep = False
    seasons = dict()

    url = play["url"]
    pattern = play["pattern"]
    episode = play["episode"]

    while not findep:
        realurl = url + "/page/" + str(page)
        print("realurl:" + realurl)
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
                        s = 1
                        if ep == episode:
                            findep = True
                            print("page:" + str(page))
                        elif ep > episode:
                            print("1080p:" + str(a.text).strip())
                            # print("ep:" + str(ep))
                            link = tr.find('a', href=re.compile('magnet:'))
                            uri = str(link['href'])

                            if s not in seasons:
                                seasons[s] = dict()
                            seasons[s][ep] = uri

        page += 1

    print("Got all episodes of {}".format(play['name']))

    seasons = OrderedDict(sorted(seasons.items()))
    for s in seasons:
        seasons[s] = OrderedDict(sorted(seasons[s].items()))
    for s in seasons:
        for ep in seasons[s]:
            uri = seasons[s][ep]
            alluri += uri + "\n\r"
            # play['season'] = season
            play['episode'] = episode

    return alluri


def output_uri():
    playlist = load_config(config_name)
    alluri = ""
    for play in playlist:
        alluri += dmhy_find_url(play)
        save_config(playlist, config_name)

    # print("alluri:\n" + alluri)
    timenow = datetime.datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists("dmhy_txt"):
        os.makedirs("dmhy_txt")
    filename = os.path.join("dmhy_txt", "zimuzu_{}.txt".format(timenow))
    print(filename)
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(alluri)


output_uri()


