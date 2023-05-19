#!/usr/bin/env python
# -*- coding: utf-8 -*-
from re import compile

# 清理多余文件
tourl, expg = compile(r'(?:url[(\'\"\s]+([^)\'\"\s]+)[)\'\"\s]+|(?:href|src)[:=\'\"\s]+([^()\'\"\s]+)[\'\"\s]+)'), compile(
    r'(?i)(?:<title></title>|colophon|logo[-_]|bookwalker[^"\n]*?\.)')


def getbsn(p, completily=False):
    if not completily:
        res = tourl.findall(p)
        return ''.join(res[0]).rsplit('/', 1)[-1] if res else p.rsplit('/', 1)[-1].strip('\'\" ')
    else:
        return {''.join(i).rsplit('/', 1)[-1] for i in tourl.findall(p)}


def clear(bk, mode='unused'):
    delitem = False
    if mode == 'misc':
        print('\n清理杂项文件……')
        for i in bk._w.other:
            if i != 'mimetype' and i != 'META-INF/container.xml' and not i.endswith('opf'):
                print('　-删除：【', i, '】', sep='')
                bk.deleteotherfile(i)
                delitem = True
        for i in bk.manifest_iter():
            if not (i[2].endswith('ml') or i[2].startswith('image')):
                print('　-删除：【', getbsn(i[1]), '】', sep='')
                bk.deletefile(i[0])
                delitem = True
    elif mode == 'page':
        print('\n清理多余文档页……')
        for i in bk.text_iter():
            if i[0] != bk.getnavid() and expg.search(bk.readfile(i[0])):
                print('　-删除：【', getbsn(i[1]), '】', sep='')
                bk.deletefile(i[0])
                delitem = True
    elif mode == 'unused':
        print('\n清理未使用的文件……')
        UNUSED = {i[0] for i in bk.manifest_iter() if not (
            i[2].startswith('application') or i[2].startswith('text'))}
        for i in bk.manifest_iter():
            if i[2].endswith('xhtml+xml') or i[2].endswith('css'):
                for j in getbsn(bk.readfile(i[0]), True):
                    UNUSED.discard(bk.basename_to_id(j))
        for i in UNUSED:
            print('　-删除：【', bk.id_to_href(i).rsplit('/', 1)[-1], '】', sep='')
            bk.deletefile(i)
            delitem = True
    if not delitem:
        print('　+无多余文件')
