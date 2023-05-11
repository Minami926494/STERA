#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fontTools.ttLib import TTFont
from fontTools.subset import load_font, Subsetter, Options
from lxml.html import document_fromstring
from css_parser.css import CSSStyleSheet
from re import compile
from io import BytesIO
from html import unescape
from .clear_core import getbsn

# 字体子集化
white_clear, html_clear, css_clear, css_import, css_link, style_font, line_font, css_clssel, css_idsel, css_regsel, font_split = compile(r'[\s　]+'), compile(r'(?s)(?:<!--(?:(?!-->).)+-->|<script(?:(?!</script>).)*?</script>|<style(?:(?!</style>).)*?</style>)'), compile(r'(?s)(?:/\*(?:(?!\*/).)+\*/|[^{}\n\r]+\{((?!font-family)[^{}])*?\})'), compile(
    r'@import\s*(.+?);'), compile(r'<link[^>]*?href="([^"]+)"'), compile(r'<style[^>]*?>((?:(?!</style>).)*?)</style>'), compile(r'font-family:\s*([^;\"\']+?)\s*(!important)?\s*[;\"\']'), compile(r'\.[A-Za-z\d*]+\s*$'), compile(r'#[A-Za-z\d*]+\s*$'), compile(r'\]\s*$'), compile(r'[\s,]+')


def subfont(bk):
    print('\n字体子集化……')
    SHEET, CSS, ID2FML, FML2ID, GLYPH, ELEM, FONT = CSSStyleSheet(), {}, {}, {
    }, {}, {}, {}
    for i in bk.css_iter():
        bsn = getbsn(i[1])
        CSS[bsn], SHEET.cssText = [], css_import.sub(lambda x: css_clear.sub('', bk.readfile(
            bk.basename_to_id(getbsn(x.group(1))))), css_clear.sub('', bk.readfile(i[0])))
        for j in SHEET.cssRules:
            try:
                if j.style.fontFamily:
                    if j.style.src:
                        a, b = bk.basename_to_id(
                            getbsn(j.style.src)), getbsn(j.style.fontFamily)
                        ID2FML[a], FML2ID[b] = b, a
                    else:
                        CSS[bsn].append(
                            (j.selectorText, j.style.fontFamily, j.style.getPropertyPriority('font-family')))
            except AttributeError:
                continue
    ID2FILE = {}.fromkeys(ID2FML, BytesIO())
    for i in bk.font_iter():
        f = BytesIO(bk.readfile(i[0]))
        if i[0] in ID2FML:
            font, ID2FILE[i[0]] = set(TTFont(f).getBestCmap()), f
            if font:
                GLYPH[ID2FML[i[0]]] = font
        else:
            print('　-删除：【', getbsn(i[1]), '】', sep='')
            bk.deletefile(i[0])
    for i in bk.text_iter():
        xh = bk.readfile(i[0])
        dom, SHEET.cssText = document_fromstring(html_clear.sub(
            '', xh).encode()), css_clear.sub('', ''.join(style_font.findall(xh)))
        STYLE = [(j.selectorText, j.style.fontFamily, j.style.getPropertyPriority(
            'font-family')) for j in SHEET.cssRules if j.style.fontFamily]
        for j in css_link.findall(xh):
            try:
                STYLE.extend(CSS[getbsn(j)])
            except:
                continue
        for j in dom.xpath('//*[contains(@style,"font-family")]'):
            m, n = line_font.search(j.get('style')).groups()
            ELEM[j] = [{j} | set(j.iterdescendants()), m, 7 if n else 3]
        for j in STYLE:
            if css_clssel.search(j[0]) or css_regsel.search(j[0]):
                im = 1
            elif css_idsel.search(j[0]):
                im = 2
            else:
                im = 0
            for k in dom.cssselect(j[0], translator='xhtml'):
                level = im+4 if j[2] else im
                if k not in ELEM or ELEM[k][2] <= level:
                    ELEM[k] = [{k} | set(k.iterdescendants()), j[1], level]
        for j, (des, fml, im) in ELEM.items():
            inherit = 'unset'
            for k in j.iterancestors():
                if k in ELEM:
                    if 'inherit' in fml:
                        inherit = ELEM[k][1]
                    if ELEM[k][2] < 4 or ELEM[k][2] <= im:
                        ELEM[k][0] -= des
            if inherit != 'unset':
                ELEM[j][1] = fml.replace('inherit', inherit)
        for j in ELEM:
            e = tuple(k for k in font_split.split(ELEM[j][1].strip(
            )) if k in GLYPH and k != 'initial' and k != 'unset' and k != 'inherit')
            if not e:
                continue
            if e not in FONT:
                FONT[e] = set()
            FONT[e].update(ord(l) for l in white_clear.sub('', unescape(
                ''.join(''.join(k.xpath('./text()')) for k in ELEM[j][0]))))
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
            return -1
        else:
            hl, file, OPT = len(has), BytesIO(), Options()
            OPT.layout_features, subsetter, font = '*', Subsetter(
                OPT), load_font(ID2FILE[fid], OPT)
            print('　+保留', str(hl), '个：【', bsn, '】=>【', has[:80], '】' if hl <= 80 else '】等', sep=''), HAS[i].add(30340), subsetter.populate(
                unicodes=HAS[i]), subsetter.subset(font), font.save(file), font.close(), bk.writefile(fid, file.getvalue()), file.close()
