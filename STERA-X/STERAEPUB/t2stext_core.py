#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from regex import compile
from .t2stext_dict import zht2s

# 繁简转换
_decode = compile(r'\0(\d+)\0')


def t2stext(bk):
    print('\n繁简转换……')
    tdic = tuple(sorted(zht2s, reverse=True, key=len))
    if bk.getmetadataxml():
        bk.setmetadataxml(t2s(bk.getmetadataxml(), tdic))
    for i in bk.text_iter():
        bk.writefile(i[0], t2s(bk.readfile(i[0]), tdic))
    print('　+繁简转换完成')


def t2s(text, tran_dict):
    for i in range(len(tran_dict)):
        text = text.replace(tran_dict[i], str(i).join(('\0', '\0')))
    return _decode.sub(lambda x: zht2s[tran_dict[int(x.group(1))]], text)
