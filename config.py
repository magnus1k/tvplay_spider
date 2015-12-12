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
