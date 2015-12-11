# -*- coding: utf-8 -*-
import requests
from collections import OrderedDict
from time import sleep
import datetime
import os


def get_url(url, headers=dict(), retries=10):
    try:
        res = requests.get(url, headers=headers)
    except Exception as what:
        print(what, url)
        if retries > 0:
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


def save_uri(filekeyword, alluri, user):
    timenow = datetime.datetime.now().strftime("%Y-%m-%d")
    userdir = os.path.join("users", user)
    if not os.path.exists(userdir):
        os.makedirs(userdir)
    filename = os.path.join(userdir, "{}_{}.txt".format(filekeyword, timenow))
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(alluri)
        return True

    return False

