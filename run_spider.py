# -*- coding: utf-8 -*-

from zimuzu_spider import ZimuzuSite
from dmhy_spider import DmhySite
import os


ZIMUZU_CONF = "zimuzu.json"
ACCOUNT_CONF = "account.json"
DMHY_CONF = "dmhy.json"

users = [name for name in os.listdir('users')
         if os.path.isdir(os.path.join('users', name))]

for user in users:
    userdir = os.path.join('users', user)
    files = [name for name in os.listdir(userdir)
             if os.path.isfile(os.path.join(userdir, name)) and name.endswith('.json')]

    if ZIMUZU_CONF in files:
        if ACCOUNT_CONF in files:
            print(os.path.join(userdir, ACCOUNT_CONF))
            site = ZimuzuSite(os.path.join(userdir, ACCOUNT_CONF))
        else:
            site = ZimuzuSite()  # I really don't know this will work or not.
        site.get_plays(os.path.join(userdir, ZIMUZU_CONF), user)

    if DMHY_CONF in files:
        site = DmhySite()
        site.get_plays(os.path.join(userdir, DMHY_CONF), user)
