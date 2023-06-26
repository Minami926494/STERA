#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import time
from logging import disable
from .gui_core import launch
from .build_core import buildtoc, buildtem
from .regrex_core import dom
from .clear_core import clear
from .t2stext_core import t2stext
from .cpsimg_core import cpsimg
from .subfont_core import subfont

version = __version__ = '1.3.3'
__all__ = ['start']


def start(bk):
    disable(), print('【虚空文学旅团STERAePub++ ver', version, '】', sep='')
    para = launch(bk)
    if para:
        st = time()
        if para['auto']:
            if para['del']:
                clear(bk, mode='misc')
            if para['tem']:
                buildtem(bk)
            if para['flow_title']:
                buildtoc(bk, mode='ctt')
            del dom(bk, para['chk'])(para['flow_class'],
                                     para['flow_tag'],
                                     para['flow_text'],
                                     para['flow_title'],
                                     para['flow_note'],
                                     para['flow_image'],
                                     para['flow_page'])
            if para['del']:
                clear(bk, mode='page')
            if para['tem']:
                buildtem(bk, para)
            if para['flow_title']:
                buildtoc(bk, mode='nav')
            if para['del']:
                clear(bk)
        if para['t2s']:
            t2stext(bk)
        if para['sub']:
            subfont(bk)
        if para['cps']:
            cpsimg(bk)
        buildtoc(bk), print('\n【运行结束，共计耗时%.2f秒】' % (time()-st))
    else:
        print('\n【运行中止】')
