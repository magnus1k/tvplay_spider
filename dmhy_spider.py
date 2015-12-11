# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from config import load_config, save_config
from collections import OrderedDict
import datetime
import os
from time import sleep


class DmhySite:
    def __init__(self):
        self.headers = dict()

    def get_headers(self):
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': user_agent}

    def get_url(self, url):
        res = requests.get(url, self.headers)
        return res.content

    def sort_plays(self, seasons):
        seasons = OrderedDict(sorted(seasons.items()))
        for season in seasons:
            seasons[season] = OrderedDict(sorted(seasons[season].items()))
        return seasons

    @staticmethod
    def last_page(text):
        lastpage = re.search("服务器遇到错误|沒有可顯示資源", text)
        if lastpage:
            return True
        else:
            return False

    def get_play_from_webpage(self, play):

        page = 1
        findep = False
        seasons = dict()

        while not findep:
            realurl = "{}&page={}".format(play["url"], str(page))
            webpage = self.get_url(realurl)
            soup = BeautifulSoup(webpage, 'html.parser')

            if DmhySite.last_page(str(soup.text)):
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
                                print("pagecount=ß" + str(page))
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

        return seasons

    def get_plays(self, config_name, user):
        playlist = load_config(config_name)

        for play in playlist:
            alluri = ""
            allname = ""

            seasons = self.sort_plays(self.get_play_from_webpage(play))

            for season in seasons:
                for episode in seasons[season]:
                    uri = seasons[season][episode]
                    alluri += uri + "\n\r"
                    allname += str(play['name']) + " ep:" + str(episode) + "\n\r"
                    # play['season'] = season
                    play['episode'] = episode

            save_config(playlist, config_name)

            timenow = datetime.datetime.now().strftime("%Y-%m-%d")
            userdir = os.path.join("users", user)
            if not os.path.exists(userdir):
                os.makedirs(userdir)
            filename_link = os.path.join(userdir, "dmhy_link{}.txt".format(timenow))
            filename_log = os.path.join(userdir, "dmhy_log{}.txt".format(timenow))
            # print(filename_link)
            with open(filename_link, 'a', encoding='utf-8') as file:
                file.write(alluri)
            with open(filename_log, 'a', encoding='utf-8') as file:
                file.write(allname)

            sleep(15)

if __name__ == "__main__":
    site = DmhySite()
    site.get_plays("users/kinkin/dmhy.json", "kinkin")
