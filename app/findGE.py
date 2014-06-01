# -*- coding:utf-8 -*-

def findByClass(all_items, classinfo):
    objs = []
    for item in all_items:
        if isinstance(item, classinfo):
            objs.append(item)
    return objs
