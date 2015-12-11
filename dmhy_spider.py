# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from config import load_config, save_config
from collections import OrderedDict
import datetime
import os
from time import sleep

config_name = "dmhy.json"

class Dmhy_site:
    def dmhy_find_url(self, play):
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}

        alluri = ""
        allname = ""
        page = 1
        findep = False
        seasons = dict()

        while not findep:
            realurl = "{}&page={}".format(play["url"], str(page))
            print("realurl:" + realurl)
            res = requests.get(realurl, headers)
            soup = BeautifulSoup(res.content, 'html.parser')

            lastpage = re.search("服务器遇到错误|沒有可顯示資源", str(soup.text))
            if lastpage:
                break

            for tr in soup.find_all('tr'):
                for a in tr.find_all('a'):
                    if a.has_attr('target') and a['target'] == '_blank':
                        match = re.search(play["pattern"], str(a.text))
                        if match:
                            ep = int(str(match.group('ep')).strip())
                            s = 1
                            if ep == play["episode"]:
                                findep = True
                                print("page:" + str(page))
                            elif ep > play["episode"]:
                                # print("1080p:" + str(a.text).strip())
                                # print("ep:" + str(ep))
                                link = tr.find('a', href=re.compile('magnet:'))
                                uri = str(link['href'])

                                if s not in seasons:
                                    seasons[s] = dict()
                                seasons[s][ep] = uri

            page += 1
            if not findep:
                sleep(15)

        print("Got all episodes of {}".format(play['name']))

        seasons = OrderedDict(sorted(seasons.items()))
        for s in seasons:
            seasons[s] = OrderedDict(sorted(seasons[s].items()))
        for s in seasons:
            for ep in seasons[s]:
                uri = seasons[s][ep]
                alluri += uri + "\n\r"
                allname += str(play['name']) + " ep:" + str(ep) + "\n\r"
                # play['season'] = season
                play['episode'] = ep

        return alluri, allname, play


    def get_plays(self, config_name, user):
        playlist = load_config(config_name)
        alluri = ""
        allname = ""
        for play in playlist:
            thisuri, thisname, play = self.dmhy_find_url(play)
            alluri += thisuri
            allname += thisname
            save_config(playlist, config_name)

            # print("alluri:\n" + alluri)
            timenow = datetime.datetime.now().strftime("%Y-%m-%d")
            userdir = os.path.join("users", user)
            if not os.path.exists(userdir):
                os.makedirs(userdir)
            filename_link = os.path.join(userdir, "dmhy_link{}.txt".format(timenow))
            filename_log = os.path.join(userdir, "dmhy_log{}.txt".format(timenow))
            print(filename_link)
            with open(filename_link, 'a', encoding='utf-8') as file:
                file.write(alluri)
            with open(filename_log, 'a', encoding='utf-8') as file:
                file.write(allname)

            sleep(15)

if __name__ == "__main__":
    get_plays("users/kinkin/dmhy.json","kinkin")
