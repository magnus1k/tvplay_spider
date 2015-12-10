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

    file_dict = list()
    js_dict = dict()
    js_dict['name'] = "名侦探柯南"
    js_dict['pattern'] = "(名侦探柯南\\s)(?P<ep>\d+).*(\\[1080[pP]\\])"
    js_dict['url'] = "https://share.dmhy.org/topics/list/team_id/75"
    js_dict['episode'] = 781
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "钻石王牌"
    js_dict['pattern'] = "(\\[钻石王牌\\]).*\\[(?P<ep>\d+)\\].*(\\[1080[pP]\\])"
    js_dict['url'] = "https://share.dmhy.org/topics/list/team_id/288"
    js_dict['episode'] = 25
    file_dict.append(js_dict)
    save_config(file_dict, "dmhy.conf")
    # js_dict = load_config("zimuzu.conf")
    # print(js_dict)
