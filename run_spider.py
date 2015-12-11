# -*- coding: utf-8 -*-
from zimuzu_spider import Zimuzu_site
from config import load_config
import os


ZIMUZU_CONF = "zimuzu.json"
ACCOUNT_CONF = "account.json"
DMHY_CONF = "dmhy.json"

users = [name for name in os.listdir('users')
            if os.path.isdir(os.path.join('users', name))]

for user in users:
    account = ""
    password = ""
    userdir = os.path.join('users',user)
    files = [name for name in os.listdir(userdir)
            if os.path.isfile(os.path.join(userdir, name)) and name.endswith('.json')]
    if ZIMUZU_CONF in files:
        if ACCOUNT_CONF in files:
            site = Zimuzu_site(os.path.join(userdir, ACCOUNT_CONF))
        else:
            site = Zimuzu_site() # I really don't know this will work or not.
        site.get_plays(os.path.join(userdir, ZIMUZU_CONF), user)

    if DMHY_CONF in files:
        
