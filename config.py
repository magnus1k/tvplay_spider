# -*- coding: utf-8 -*-

import json


def load_config(filename):
    with open(filename, encoding='utf-8') as file:
        text = file.read()
        js = json.loads(text)
        return js


def save_config(json_dict, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        text = json.dumps(json_dict, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        file.write(text)

if __name__ == "__main__":
    file_dict = list()
    js_dict = dict()
    js_dict['name'] = "冰与火之歌"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/10733"
    js_dict['season'] = 5
    js_dict['episode'] = 10
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "生活大爆炸"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/11005"
    js_dict['season'] = 9
    js_dict['episode'] = 9
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "摩登家庭"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/11010"
    js_dict['season'] = 7
    js_dict['episode'] = 6
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "Community"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/11018"
    js_dict['season'] = 6
    js_dict['episode'] = 13
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "破产姐妹"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/11103"
    js_dict['season'] = 5
    js_dict['episode'] = 3
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "Dr Ken"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/33666"
    js_dict['season'] = 1
    js_dict['episode'] = 7
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "Supergirl"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/33549"
    js_dict['season'] = 1
    js_dict['episode'] = 5
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "疑犯追踪"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/11009"
    js_dict['season'] = 5
    js_dict['episode'] = 0
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "Supernatural"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/11015"
    js_dict['season'] = 10
    js_dict['episode'] = 0
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "Flash"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/32235"
    js_dict['season'] = 2
    js_dict['episode'] = 0
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "绿箭"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/32235"
    js_dict['season'] = 3
    js_dict['episode'] = 3
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "哥谭"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/32097"
    js_dict['season'] = 1
    js_dict['episode'] = 3
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "灵书妙探"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/10996"
    js_dict['season'] = 7
    js_dict['episode'] = 6
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "硅谷"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/31801"
    js_dict['season'] = 2
    js_dict['episode'] = 0
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "南方公园"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/10490"
    js_dict['season'] = 18
    js_dict['episode'] = 5
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "格林"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/11080"
    js_dict['season'] = 4
    js_dict['episode'] = 0
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "演绎法"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/26898"
    js_dict['season'] = 3
    js_dict['episode'] = 0
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "神盾局特工"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/30675"
    js_dict['season'] = 3
    js_dict['episode'] = 0
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "纸牌屋"
    js_dict['url'] = "http://www.zimuzu.tv/resource/list/28793"
    js_dict['season'] = 1
    js_dict['episode'] = 0
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
    js_dict['episode'] = 34
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "海贼王"
    js_dict['pattern'] = "(\\[ONE PIECE 海贼王\\]).*\\[第(?P<ep>\d+)话\\].*(\\[1080[pP]\\])"
    js_dict['url'] = "https://share.dmhy.org/topics/list/team_id/34"
    js_dict['episode'] = 680
    file_dict.append(js_dict)

    js_dict = dict()
    js_dict['name'] = "银魂"
    js_dict['pattern'] = "(\\[银魂\\]).*\\[(?P<ep>\d+)\\].*(\\[1080[pP].*\\])"
    js_dict['url'] = "https://share.dmhy.org/topics/list/team_id/117"
    js_dict['episode'] = 289
    file_dict.append(js_dict)

    save_config(file_dict, "dmhy.conf")
    # js_dict = load_config("zimuzu.conf")
    # print(js_dict)
