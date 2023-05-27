#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from regex import compile
from io import BytesIO
from PIL import Image
from .clear_core import getbsn

# 图片压缩
catchimg = compile(
    r'<body[^一-龥あ-ヶー]*?<ima?ge?[^>]*?(?:src|href)="[^"]*?([^"/]+)"[^>]*?/>(?:(?!<img|<image)[^一-龥あ-ヶー])*?/body>')


def getpic(bk):
    for i in bk.text_iter():
        catch = catchimg.search(bk.readfile(i[0]))
        if catch:
            yield i[0], bk.basename_to_id(catch.group(1))


def cpsimg(bk):
    print('\n图片压缩……')
    IMG = {}
    for i in bk.image_iter():
        bsn = getbsn(i[1])
        if i[0] == tuple(getpic(bk))[0][1]:
            img = cps(bk.readfile(i[0]), bsn.rsplit('.', 1)[-1], 'jpeg')
            if img:
                print('　+压缩：【', bsn, '】', sep='')
            else:
                print('　-未压缩：【', bsn, '】', sep='')
                continue
            if i[1].endswith('jpg'):
                bk.writefile(i[0], img)
            else:
                bk.deletefile(i[0])
                n = bsn.rsplit('.', 1)[0]
                while 1:
                    name = ''.join((n, '.jpg'))
                    try:
                        bk.addfile(i[0], name, img, 'image/jpeg')
                        IMG[bsn] = name
                        break
                    except:
                        n += '_'
        else:
            img = cps(bk.readfile(i[0]), bsn.rsplit('.', 1)[-1])
            if img:
                print('　+压缩：【', bsn, '】', sep='')
            else:
                print('　-未压缩：【', bsn, '】', sep='')
                continue
            if i[1].endswith('webp'):
                bk.writefile(i[0], img)
            else:
                bk.deletefile(i[0])
                n = bsn.rsplit('.', 1)[0]
                while 1:
                    name = ''.join((n, '.webp'))
                    try:
                        bk.addfile(i[0], name, img, 'image/webp')
                        IMG[bsn] = name
                        break
                    except:
                        n += '_'
    for i in sorted(IMG, reverse=True, key=len):
        for j in bk.manifest_iter():
            if j[2].endswith(('xhtml+xml', 'css')):
                bk.writefile(j[0], bk.readfile(j[0]).replace(i, IMG[i]))


def cps(img, fm=None, tofm='webp'):
    pic, bsize = Image.open(BytesIO(img)), len(img)
    size, img = pic.size, BytesIO()
    if max(size) > 2048:
        pic.resize((2048, int(size[1]*2048/size[0])) if size[0]
                   >= size[1] else (int(size[0]*2048/size[1]), 2048))
    pic.save(img, tofm, optimize=True, quality=80)
    image = img.getvalue()
    img.close()
    return image if bsize/len(image) >= 1.1 or fm != tofm else None
