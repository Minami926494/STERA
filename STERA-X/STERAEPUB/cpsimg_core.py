#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from regex import compile
from PIL import Image
from io import BytesIO
from multiprocessing import Pool
try:
    from .bookenv_core import book, getbsn
except ImportError:
    from bookenv_core import book, getbsn

# 图片压缩
catchimg = compile(
    r'<body[^一-龥あ-ヶー]*?<ima?ge?[^>]*?(?:[^-]src|href)="[^"]*?([^"/]+)"[^>]*?/>(?:(?!<img|<image)[^一-龥あ-ヶー])*?/body>')


def getpic(bk: book):
    for ele in bk.iter('text'):
        catch = catchimg.search(ele.read())
        if catch:
            pic = bk.get(bsn=getbsn(catch.group(1)))
            if pic:
                yield ele, pic


def cpsimg(bk):
    print('\n图片压缩……')
    PIC, IMG, pool = {}, {}, Pool()
    for i in bk.image_iter():
        bsn = getbsn(i[1])
        if i[0] == getpic(bk)[1]:
            PIC[(i[0], bsn, True)] = pool.apply_async(cps, args=(
                bk.readfile(i[0]), bsn.rsplit('.', 1)[-1], 'jpeg'))
        else:
            PIC[(i[0], bsn, False)] = pool.apply_async(
                cps, args=(bk.readfile(i[0]), bsn.rsplit('.', 1)[-1]))
    pool.close(), pool.join()
    for (pid, bsn, cover), img in PIC.items():
        img, (ext, mime) = img.get(), ('jpg',
                                       'image/jpeg') if cover else ('webp', 'image/webp')
        if img:
            print('　+压缩：【', bsn, '】', sep='')
        else:
            print('　-未压缩：【', bsn, '】', sep='')
            continue
        if bsn.endswith(ext):
            bk.writefile(pid, img)
        else:
            bk.deletefile(pid)
            n = bsn.rsplit('.', 1)[0]
            while 1:
                name = '.'.join((n, ext))
                try:
                    bk.addfile(pid, name, img, mime)
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
    pic.save(img, tofm, optimize=True, quality=80 if bsize > 100000 else 90)
    image = img.getvalue()
    img.close()
    return image if bsize/len(image) >= 1.1 or (fm != 'webp' if tofm == 'webp' else fm != 'jpg') else None
