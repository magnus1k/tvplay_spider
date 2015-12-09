# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re


def dmhy_find_url(url, pattren, episode):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    res = requests.get(url, headers)
    # print(res.content)
    soup = BeautifulSoup(res.content, 'html.parser')
    for tr in soup.find_all('tr'):
        for a in tr.find_all('a'):
            if a.has_attr('target') and a['target'] == '_blank':
                match = re.search(pattren, str(a.text))
                if match:
                    ep = int(str(match.group('ep')).strip())
                    if ep > episode:
                        print("1080p:" + str(a.text).strip())
                        print("ep:" + str(ep))
                        link = tr.find('a', href=re.compile('magnet:'))
                        print("link:" + link['href'])

dmhy_find_url("https://share.dmhy.org/topics/list/team_id/75", '(名侦探柯南\\s)(?P<ep>\d+).*(\\[1080[pP]\\])', 770)


