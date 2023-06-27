#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from regex import compile
try:
    from .bookenv_core import book
    from .t2stext_dict import zht2s
except ImportError:
    from bookenv_core import book
    from t2stext_dict import zht2s

# 繁简转换
_decode = compile(r'\0(\d+)\0')


def t2stext(bk: book):
    print('\n繁简转换……')
    tdic = tuple(sorted(zht2s, reverse=True, key=len))
    if bk.metadata:
        bk.metadata = t2s(bk.metadata, tdic)
    for ele in bk.iter('text'):
        ele.write(t2s(ele.read(), tdic))
    print('　+繁简转换完成')


def t2s(text: str, tran_dict: tuple):
    for i in range(len(tran_dict)):
        text = text.replace(tran_dict[i], str(i).join(('\0', '\0')))
    return _decode.sub(lambda x: zht2s[tran_dict[int(x.group(1))]], text)
