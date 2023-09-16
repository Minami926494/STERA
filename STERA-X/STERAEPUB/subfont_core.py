#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fontTools.ttLib import TTFont, TTCollection
from fontTools.subset import load_font, Subsetter, Options
from lxml.html import HTMLParser, document_fromstring
from css_parser.parse import CSSParser
from regex import compile
from os.path import join, dirname
from multiprocessing import Pool
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
    CHANGE, GLYPH, HAS, LOSS = {}, {}, {}, {}
    for ele in bk.iter('font'):
        HAS[ele], LOSS[ele], stdbsn = set(), set(), ele.name+'.ttf'
        try:
            ttf = TTFont(ele.fp)
        except:
            ttf = TTCollection(ele.fp).fonts[0]
        if ele.bsn != stdbsn:
            CHANGE[ele.bsn] = stdbsn
            fp = join(dirname(ele.fp), stdbsn)
            bk.delete(ele)
            ttf.save(fp)
            ele = bk.set(bk.elem(fp))
        ele.cmap = set(ttf.getBestCmap())
        ttf.close()
    OLD = sorted(CHANGE, reverse=True, key=len)
    for ele in bk.iter('css'):
        data = ele.read()
        for aim in OLD:
            data = data.replace(aim, CHANGE[aim])
        ele.write(data)
        sheet, ele.imp, ele.font, style = CSSParser(
            loglevel='CRITICAL', parseComments=False, validate=False).parseString(data).cssRules, [], {}, {}
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
    for ele in bk.iter('text'):
        dom, csssel, cssfont, tree = document_fromstring(ele.read(True), HTMLParser(
            remove_blank_text=True, remove_comments=True, remove_pis=True)), {}, {}, {}
        for i in dom.xpath('//link'):
            css = bk.get(bsn=first(getbsn(i.get('href'))))
            if css:
                for imp in css.imp:
                    csssel.update(imp.sel)
                    cssfont.update(imp.font)
                csssel.update(css.sel)
                cssfont.update(css.font)
        for i in dom.xpath('//style'):
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
        for i in dom.xpath('//*[contains(@style,"font-family")]'):
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
        calc(dom.xpath('//body')[0])
    for src, text in GLYPH.items():
        text = set(map(ord, unescape(text)))
        for font in src:
            has = text & font.cmap
            HAS[font] |= has
            text -= has
            if not text:
                HAS[font] |= set(range(32, 126))  # 末位字体保留ASCII字符
                break
        if text:
            for font in src:
                LOSS[font] |= text
    pool = Pool()
    for ele in bk.iter('font'):
        has, loss = HAS.get(ele), LOSS.get(ele)
        if loss:
            ll = len(loss)
            print('　-缺字', str(ll), '个：【', ele.bsn, '】=>',
                  loss[:80], '' if ll <= 80 else '等', sep='')
        elif has:
            hl = len(has)
            has.add(30340)
            pool.apply_async(sbf, args=(ele, has))
            print('　+保留', str(hl), '个：【', ele.bsn, '】=>',
                  has[:80], '' if hl <= 80 else '等', sep='')
        else:
            print('　-删除：【', ele.bsn, '】', sep='')
            bk.delete(ele)
    pool.close(), pool.join()


def sbf(ele: book.elem, used: set):
    OPT, fp = Options(), ele.fp
    OPT.layout_features, OPT.glyph_names, OPT.desubroutinize, OPT.drop_tables, OPT.flavor, subsetter, font = '*', True, True, [
        'DSIG'], 'woff2', Subsetter(OPT), load_font(fp, OPT)
    subsetter.populate(unicodes=used), subsetter.subset(
        font), font.save(fp), font.close()
