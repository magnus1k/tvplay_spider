# -*- coding: utf-8 -*-

import json


def load_config(filename):
    with open(filename, encoding='utf-8') as file:
        text = file.read()
        js = json.loads(text)
        return js


def save_config(json_dict, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        text = json.dumps(json_dict)
        file.write(text)

if __name__ == "__main__":
    file_dict = list()
    js_dict = dict()
    js_dict['name'] = "冰与火之歌"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/10733"
    js_dict['season'] = 3
    js_dict['episode'] = 1
    file_dict.append(js_dict)
    save_config(file_dict, "zimuzu.conf")
    # js_dict = load_config("zimuzu.conf")
    # print(js_dict)
