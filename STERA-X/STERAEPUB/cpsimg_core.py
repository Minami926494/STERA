#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from regex import compile
from PIL import Image
from io import BytesIO
from multiprocessing import Pool
try:
    from .bookenv_core import book, InvalidEpubError, getbsn
except ImportError:
    from bookenv_core import book, InvalidEpubError, getbsn

# 图片压缩
catchimg = compile(
    r'<body[^一-龥あ-ヶー]*?<ima?ge?[^>]*?(?:[^-]src|href)="[^"]*?([^"/]+)"[^>]*?/>(?:(?!<img|<image)[^一-龥あ-ヶー])*?/body>')


def getpic(bk: book):
    '''
    传入book对象，返回包含HTML文档中所有图片独占页及对应图片的elem对象的生成器。\n
    bk -> EPUB的book对象
    '''
    for ele in bk.iter('text'):
        catch = catchimg.search(ele.read())
        if catch:
            pic = bk.get(bsn=getbsn(catch.group(1)))
            if pic:
                yield ele, pic


def cpsimg(bk: book):
    '''
    传入book对象，对HTML文档中使用的图片文件进行压缩，将封面压缩为jpg格式，其余压缩为webp格式，并修改文中的对应链接。\n
    bk -> EPUB的book对象
    '''
    print('\n图片压缩……')
    PIC, IMG, pool = {}, {}, Pool()
    for ele, pic in getpic(bk):
        cover = pic
        break
    else:
        raise InvalidEpubError('未找到有效的封面图片')
    for ele in bk.iter('image'):
        PIC[ele] = pool.apply_async(cps, args=(
            ele, 'jpeg' if ele is cover else 'webp'))
    pool.close(), pool.join()
    for ele, img in PIC.items():
        img, bsn, stdext = img.get(), ele.bsn, '.jpg' if ele is cover else '.webp'
        if img:
            print('　+压缩：【', bsn, '】', sep='')
        else:
            print('　-未压缩：【', bsn, '】', sep='')
            continue
        if bsn.endswith(stdext):
            ele.write(img)
        else:
            stdbsn = ele.name+stdext
            IMG[bsn] = stdbsn
            bk.delete(ele)
            bk.set(bk.add(stdbsn, img))
    changed = sorted(IMG, reverse=True, key=len)
    for ele in bk.iter('text', 'css'):
        data = ele.read()
        for i in changed:
            if i in data:
                ele.write(data.replace(i, IMG[i]))


def cps(img: book.elem, tofm: str = 'webp'):
    '''
    通过传入图片的elem对象和目标格式对图片进行压缩，使图片长边不超过2048px，并根据体积是否超过100kb将图片质量压缩为80/90。\n
    img -> 目标图片的elem对象\n
    tofm -> 图片的目标格式，默认为webp
    '''
    pic, fm, res = Image.open(img.fp), img.ext[1:], BytesIO()
    size, bsize = pic.size, len(img)
    if max(size) > 2048:
        pic.resize((2048, int(size[1]*2048/size[0])) if size[0]
                   >= size[1] else (int(size[0]*2048/size[1]), 2048))
    pic.save(res, tofm, optimize=True, quality=80 if bsize > 100000 else 90)
    image = res.getvalue()
    res.close()
    return image if bsize/len(image) >= 1.1 or (fm != 'webp' if tofm == 'webp' else fm != 'jpg') else None
