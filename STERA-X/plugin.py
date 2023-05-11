#!/usr/bin/env python
# -*- coding: utf-8 -*-
from STERAEPUB import start


def run(bk):
    if bk.launcher_version() <= 20210722:
        print('Sigil版本过低，请更新至Sigil1.8.0+！')
        return -1
    elif not bk.epub_is_standard():
        print('文档不符合Sigil规范，请先执行规范化！')
        return -1
    elif not bk.epub_version().startswith('3'):
        print('文件不是有效的EPUB3文档，请先转换至EPUB3！')
        return -1
    else:
        start(bk)
        return 0


if __name__ == '__main__':
    print('程序运行环境异常！')
    exit(-1)
