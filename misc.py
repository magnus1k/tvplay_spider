# -*- coding: utf-8 -*-
import requests
from collections import OrderedDict
from time import sleep

def get_url(url, headers=dict(), retries=10):
    try:
        res = requests.get(url, headers=headers)
    except Exception as what:
        print(what, url)
        if retries>0:
            sleep(3)
            return get_url(url, headers, retries-1)
        else:
            print('GET Failed {}'.format(url))
            raise
    return res.content

def sort_plays(seasons):
    seasons = OrderedDict(sorted(seasons.items()))
    for season in seasons:
        seasons[season] = OrderedDict(sorted(seasons[season].items()))
    return seasons
