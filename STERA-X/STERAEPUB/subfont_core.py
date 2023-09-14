#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from turtle import goto
from fontTools.ttLib import TTFont, TTCollection
from fontTools.subset import load_font, Subsetter, Options
from lxml.html import XHTMLParser, document_fromstring
from css_parser.parse import CSSParser
from regex import compile
from os.path import join, dirname
from multiprocessing import Pool
from collections.abc import Iterable
from io import BytesIO
from html import unescape
try:
    from .bookenv_core import book, getbsn, first
except ImportError:
    from bookenv_core import book, getbsn, first

# 字体子集化
white_clear, html_line, css_splitsel, css_clssel, css_idsel, css_regsel, font_split = compile(r'[\s　]+'), compile(r'font-family:\s*([^;\"\']+?)\s*(!important)?\s*(?:[;\"\']|$)'), compile(
    r'[ >]+'), compile(r'\.[A-Za-z\d*]+\s*$'), compile(r'#[A-Za-z\d*]+\s*$'), compile(r'\]\s*$'), compile(r'\s*,\s*')


def subfont(bk: book):
    print('\n字体子集化……')
    GLYPH = {}
    for ele in bk.iter('css'):
        sheet, ele.imp, ele.font, style = CSSParser(
            loglevel='CRITICAL', parseComments=False, validate=False).parseString(ele.read()).cssRules, [], {}, {}
        for i in sheet:
            if i.type == 3:
                imp = bk.get(bsn=first(getbsn(i.href)))
                if imp and imp not in ele.imp:
                    ele.imp.append(imp)
            elif hasattr(i, 'style'):
                fml = i.style.fontFamily
                if fml:
                    fml = fml.strip('\'" ')
                    if i.type == 5:
                        src = []
                        for bsn in getbsn(i.style.src):
                            font = bk.get(bsn=bsn)
                            if font:
                                src.append(font)
                        if src:
                            ele.font[fml] = src
                    elif i.type == 1:
                        sel = i.selectorText
                        for part in css_splitsel.split(sel):
                            im = 0
                            if part.startswith(tuple('abcdefghijklmnopqrstuvwxyz*')):
                                im += 1
                            if css_clssel.search(part) or css_regsel.search(part):
                                im += 10
                            if css_idsel.search(part):
                                im += 100
                        style[sel] = (font_split.split(
                            fml), im+10000 if i.style.getPropertyPriority('font-family') else im)
        for i, j in style.items():
            for k in j[0]:
                if k not in ele.font:
                    j[0].remove(k)
        ele.sel = style
    for ele in bk.iter('font'):
        try:
            cmap = set(TTFont(ele.fp).getBestCmap())
        except:
            fc, bsn = TTCollection(ele.fp).fonts[0], ele.name+'.ttf'
            cmap, fp = set(fc.getBestCmap()), join(dirname(ele.fp), bsn)
            bk.delete(ele)
            fc.save(fp)
            ele = bk.set(bk.elem(fp))
        ele.cmap = cmap
    ns = {'ns': 'http://www.w3.org/1999/xhtml'}
    for ele in bk.iter('text'):
        dom, csssel, cssfont, tree = document_fromstring(ele.read(True), XHTMLParser(
            ns_clean=True, recover=True, remove_comments=True)), {}, {}, {}
        for i in dom.xpath('//ns:link', namespaces=ns):
            css = bk.get(bsn=first(getbsn(i.get('href'))))
            if css:
                for imp in css.imp:
                    csssel.update(imp.sel)
                    cssfont.update(imp.font)
                csssel.update(css.sel)
                cssfont.update(css.font)
        for i in dom.xpath('//ns:style', namespaces=ns):
            sheet = CSSParser(loglevel='CRITICAL', parseComments=False,
                              validate=False).parseString(i.text).cssRules
            for rule in sheet:
                if rule.type == 1:
                    fml = rule.style.fontFamily
                    if fml:
                        fml, sel = fml.strip(), rule.selectorText
                        for part in css_splitsel.split(sel):
                            im = 100
                            if part.startswith(tuple('abcdefghijklmnopqrstuvwxyz*')):
                                im += 1
                            if css_clssel.search(part) or css_regsel.search(part):
                                im += 10
                            if css_idsel.search(part):
                                im += 100
                        if sel not in csssel or im >= csssel[sel][1]:
                            font = []
                            for f in font_split.split(fml):
                                src = cssfont.get(f)
                                if src:
                                    font.extend(src)
                            if font:
                                csssel[sel] = (
                                    font, im+10000 if rule.style.getPropertyPriority('font-family') else im)
        for i in dom.xpath('//ns:*[contains(@style,"font-family")]', namespaces=ns):
            (fml, im), font = html_line.search(i.get('style')).groups(), []
            for f in font_split.split(fml):
                src = cssfont.get(f)
                if src:
                    font.extend(src)
            tree[i] = (font, 11000 if im else 1000)
        for sel, style in csssel.items():
            for i in dom.cssselect(sel, translator='xhtml'):
                if i not in tree or style[1] > tree[i][1]:
                    tree[i] = style

        def calc(node, inherit=None):
            style = tree.get(node)
            if style and (not inherit or inherit[1] < 10000 or style[1] > 10000):
                inherit = style
            if inherit:
                src = tuple(set(inherit[0]))
                value = GLYPH.get(src)
                for i in node.xpath('./text()'):
                    GLYPH[src] = i+value if value else i
            for child in node.iterchildren():
                calc(child, inherit)
        calc(dom.xpath('//ns:body', namespaces=ns)[0])
    for src, text in GLYPH.items():
        pass
    HAS, LOSS = {}.fromkeys(GLYPH, set()), {}.fromkeys(GLYPH, set())
    for i1, i2 in FONT.items():
        for j in i1:
            if i2:
                has = i2 & GLYPH[j]
                HAS[j] = HAS[j] | has
                i2 -= has
            else:
                break
        else:
            LOSS[i1[-1]] = LOSS[i1[-1]] | i2
    pool = Pool()
    for i in GLYPH:
        fid, has, loss = FML2ID[i], ''.join(
            chr(j) for j in HAS[i]), ''.join(chr(j) for j in LOSS[i])
        bsn = bk.id_to_href(fid).rsplit('/', 1)[-1]
        if not has:
            print('　-删除：【', bsn, '】', sep='')
            bk.deletefile(fid)
        elif loss:
            ll = len(loss)
            print('　-缺字', str(ll), '个：【', bsn, '】=>【',
                  loss[:80], '】' if ll <= 80 else '】等', sep='')
        else:
            hl = len(has)
            HAS[i].add(30340)
            CHANGED[(fid, bsn)] = pool.apply_async(
                sbf, args=(ID2FILE[fid], HAS[i]))
            print('　+保留', str(hl), '个：【', bsn, '】=>【',
                  has[:80], '】' if hl <= 80 else '】等', sep='')
    pool.close(), pool.join()
    for (fid, bsn), file in CHANGED.items():
        n, f = bsn.rsplit('.', 1)
        if f == 'ttf':
            bk.writefile(fid, file.get())
        else:
            nbsn = ''.join((n, '.ttf'))
            bk.deletefile(fid), bk.addfile(fid, nbsn, file.get())
            for j in bk.iter('text', 'css'):
                inner = bk.readfile(j[0])
                if bsn in inner:
                    bk.writefile(j[0], inner.replace(bsn, nbsn))


def sbf(f, d):
    OPT, file = Options(), BytesIO()
    OPT.layout_features, OPT.glyph_names, OPT.desubroutinize, OPT.drop_tables, OPT.flavor, subsetter, font = '*', True, True, [
        'DSIG'], 'woff2', Subsetter(OPT), load_font(f, OPT)
    subsetter.populate(unicodes=d), subsetter.subset(
        font), font.save(file), font.close()
    subsetter.get
    font = file.getvalue()
    file.close()
    return font
