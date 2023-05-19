#!/usr/bin/env python
# -*- coding: utf-8 -*-
from re import compile
from os import path, walk
from .clear_core import getbsn
from .regrex_core import bs, reg
from .cpsimg_core import getpic

# EPUB重构
olwrap, tunwrap, tit, bookid = compile(r'(?s)<ol>\s*(.*?)\s*</ol>$'), compile(r'(?:[\n\r]+ *(?=[^< ])|\s*\\?(?= )|\s*(?=</a>))'), compile(
    r'<dc:title.*?>(.*?)</dc:title>'), compile(r'<dc:identifier.*?id="BookId".*?>(.*?)</dc:identifier>')
buildncx = ('', '', ('', {r'<a[^>]*href="[^"]*?([^"/]+)"[^>]*>\s*(.*?)\s*</a>': r'<navLabel>\n<text>\2</text>\n</navLabel>\n<content src="Text/\1"/>',
            r'</li>(?:\s*</ol>)?': '</navPoint>', r'(*)^([\s\S]*?)(?:<ol[^>]*>\s*)?<li[^>]*>': r'\1<navPoint id="navPoint*">'}))
buildxml = {'META-INF/com.apple.ibooks.display-options.xml': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<display_options>\n<platform name="*">\n<option name="specified-fonts">true</option>\n</platform>\n</display_options>',
            'META-INF/zhangyue-expansion.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<zhangyue-expansion version="3.4.2">\n<book_id></book_id>\n</zhangyue-expansion>'}


def gettype(bk, etype):
    if bk._w.guide:
        for i in bk._w.guide:
            if etype == i[0]:
                return i[2].rsplit('/', 1)[-1]
    return ''


def getdepth(soup):
    def _ (soup, level=0):
        if soup:
            level += 1
            for i in soup.findAll('li', recursive=False):
                _(i.ol, level)
        else:
            depth.add(level)
    depth = {0}
    _(soup)
    return max(depth)


def buildtoc(bk, mode='ncx'):
    navid = bk.getnavid()
    NAV = bs(bk.readfile(navid))
    toc, guide = NAV.find('nav', {'epub:type': 'toc'}).ol, NAV.find(
        'nav', {'epub:type': 'landmarks'})
    if mode == 'ctt':
        print('\n生成目录页……')
        for i in toc('li'):
            i.name, i['class'] = 'ctt', 'toc'
            for j in i('ol'):
                j.name, j['class'] = 'ctt', 'part'
        for i in toc('a'):
            i.string.wrap(NAV.new_tag('ch'))
        toc = olwrap.sub(r'<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xml="http://www.w3.org/XML/1998/namespace">\n<head>\n<title>目錄</title>\n<link href="../Styles/stylesheet.css" type="text/css" rel="stylesheet"/>\n<script type="text/javascript" src="../Misc/script.js"></script>\n</head>\n<body>\n<h3 class="ctt">Contents</h3>\n\1\n</body>\n</html>', str(toc))
        if guide and guide.find('a', {'epub:type': 'toc'}):
            bk._w.guide = [('toc', '目錄', bk.id_to_href(build(bk, bk.basename_to_id(getbsn(
                guide.find('a', {'epub:type': 'toc'})['href'])), toc, 'application/xhtml+xml')))]
        else:
            bk._w.guide = [('toc', '目錄', bk.id_to_href(
                build(bk, 'contents.xhtml', toc, 'application/xhtml+xml')))]
            bk.spine_insert_before(0, 'contents.xhtml', 'yes')
    elif mode == 'nav':
        print('\n重构NAV……')
        cover, ctt, intro = bk.id_to_href(tuple(getpic(bk))[0][0]).rsplit(
            '/', 1)[-1], gettype(bk, 'toc'), gettype(bk, 'introduction')
        nav = bs(bk.readfile(bk.basename_to_id(ctt)))
        for i in nav.body('p'):
            if i.has_attr('class') and 'ctit' in i['class']:
                i.string = ''.join(('\\ ', i.string))
            i.unwrap()
        for i in nav.body(class_=['toc', 'part']):
            i.name = 'li' if 'toc' in i['class'] else 'ol'
            del i['class']
        bk.writefile(navid, bs(''.join(('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xml="http://www.w3.org/XML/1998/namespace">\n<head>\n<title>導航</title>\n<link href="../Styles/stylesheet.css" type="text/css" rel="stylesheet"/>\n<script type="text/javascript" src="../Misc/script.js"></script>\n</head>\n<body epub:type="frontmatter" id="nav">\n<nav epub:type="toc" id="toc" role="doc-toc">\n<ol>\n<li><a href="', cover,
                     '">封面</a></li>\n<li><a href="title.xhtml">標題</a></li>\n<li><a href="message.xhtml">製作信息</a></li>', intro.join(('\n<li><a href="', '">簡介</a></li>')) if intro else '', '\n<li><a href="', ctt, '">目錄</a></li>\n', tunwrap.sub('', '\n'.join(str(i) for i in nav.body('li', recursive=False))), '\n</ol>\n</nav>\n<nav epub:type="landmarks" id="landmarks" hidden="">\n<ol>\n<li><a epub:type="cover" href="', cover, '">封面</a></li>', intro.join(('\n<li><a epub:type="introduction" href="', '">簡介</a></li>')) if intro else '', '\n<li><a epub:type="toc" href="', ctt, '">目錄</a></li>\n</ol>\n</nav>\n</body>\n</html>')), True))
        print('　+重构：【', bk.id_to_href(navid).rsplit('/', 1)[-1], '】', sep='')
    else:
        print('\n生成NCX与GUIDE……')
        meta = bk.getmetadataxml()
        title, bid = tit.search(meta).group(1) if tit.search(
            meta) else '', bookid.search(meta).group(1) if bookid.search(meta) else ''
        NCX, bk._w.group_paths['ncx'] = '\n'.join(('<?xml version="1.0" encoding="utf-8"?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n<head>', bid.join(('<meta name="dtb:uid" content="', '"/>')), str(getdepth(toc)).join(
            ('<meta name="dtb:depth" content="', '"/>')), title.join(('<meta name="dtb:totalPageCount" content="0"/>\n<meta name="dtb:maxPageNumber" content="0"/>\n</head>\n<docTitle>\n<text>', '</text>\n</docTitle>\n<navMap>')), reg(str(toc), buildncx, False), '</navMap>\n</ncx>')), ['OEBPS']
        build(bk, 'toc.ncx', NCX, 'application/x-dtbncx+xml')
        bk._w.guide, bk._w.modified[bk.get_opfbookpath()] = [(i['epub:type'], i.string, bk.id_to_href(
            bk.basename_to_id(getbsn(i['href'])))) for i in guide.findAll('a')] if guide else [], 'file'


def buildtem(bk, info=None):
    if info:
        print('\n生成信息页……')
        titid, mesid, sumid = build(bk, 'title.xhtml', ''.join(('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xml="http://www.w3.org/XML/1998/namespace">\n<head>\n<title>標題</title>\n<link href="../Styles/stylesheet.css" type="text/css" rel="stylesheet"/>\n<script type="text/javascript" src="../Misc/script.js"></script>\n</head>\n<body>\n<div class="title">\n<div class="center" style="margin:4em auto 0;">\n<p class="tilh em18 bold">', info['tit'], '</p>\n', info['stit'].join(('<p class="tilh em09 bold" style="margin:1em 0 0;">～', '～</p>\n')) if info['stit'] else '', '</div>\n<div class="center" style="margin:3em auto 4em;">\n', info['vol'].join(('<p class="tilh em15 bold">',  '</p>\n')) if info['vol'] else '', '</div>\n<div class="center">\n<p class="tilh em07 bold">作者</p>\n<p class="tilh em11 bold" style="margin:0.2em 0 0.75em;">', info['writer'], '</p>\n<p class="tilh em07 bold">插畫</p>\n<p class="tilh bold" style="margin:0.15em 0 0;">', info['painter'], '</p>\n</div>\n</div>\n</body>\n</html>'))), build(bk, 'message.xhtml', ''.join(('<div class="message">\n<div>\n<div class="meg">\n<p>製 作 信 息</p>\n</div>\n<div class="meghr"/>\n<div class="creator">\n<p>作者</p>\n</div>\n<div>\n<p>', info['writer'], '</p>\n</div>\n<div class="creator">\n<p>插畫</p>\n</div>\n<div>\n<p>', info['painter'], '</p>\n</div>\n<div class="creator">\n<p>譯者</p>\n</div>\n<div>\n<p>', info[
            'translator'], '</p>\n</div>\n<div class="creator">\n<p>圖源</p>\n</div>\n<div>\n<p>', info['introducer'], '</p>\n</div>\n<div class="creator">\n<p>錄入</p>\n</div>\n<div>\n<p>', info['inputer'], '</p>\n</div>\n<div class="group">\n<p><a href="https://www.lightnovel.us">輕之國度錄入組</a>×<a href="https://www.voidlord.com">虛空文學旅團</a></p>\n</div>\n<div class="logo">\n<img alt="logo" src="../Images/logo.png" zy-enlarge-src="none"/>\n</div>\n</div>\n</div>')).join(('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xml="http://www.w3.org/XML/1998/namespace">\n<head>\n<title>製作信息</title>\n<link href="../Styles/stylesheet.css" type="text/css" rel="stylesheet"/>\n<script type="text/javascript" src="../Misc/script.js"></script>\n</head>\n<body>\n', '\n</body>\n</html>'))), build(bk, 'summary.xhtml', info['summary'].join(('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xml="http://www.w3.org/XML/1998/namespace">\n<head>\n<title>簡介</title>\n<link href="../Styles/stylesheet.css" type="text/css" rel="stylesheet"/>\n<script type="text/javascript" src="../Misc/script.js"></script>\n</head>\n<body>\n<div class="summary">\n<h3>簡介</h3>\n<hr/>\n', '\n</div>\n</body>\n</html>'))) if info['summary'] else ''
        if sumid:
            bk._w.guide.append(('introduction', '簡介', bk.id_to_href(sumid)))
        print('\n重构OPF……')
        title, cover, picpg = info['stit'].join(('～', '～')).join((info['tit'], info['vol'])).strip(
        ) if info['stit'] else ' '.join((info['tit'], info['vol'])).strip(), None, set()
        for i1, i2 in getpic(bk):
            if cover:
                picpg.add(i1)
            else:
                cover = i1, i2
        bk.setmetadataxml('\n'.join((info['isbn'].join(('<dc:identifier id="BookId">urn:isbn:', '</dc:identifier>')), title.join(('<dc:title id="title">', '</dc:title>')), '\n'.join(('<meta property="belongs-to-collection" id="num">', info['tit'], '</meta>\n<meta refines="#num" property="collection-type">series</meta>\n<meta refines="#num" property="group-position">', info['vol'], '</meta>', info['writer'].join(('<dc:creator id="create">', '</dc:creator>')), info['epuber'].join(('<dc:contributor>', '</dc:contributor>')))) if info['vol'] else info['epuber'].join(('<dc:contributor>', '</dc:contributor>')),  cover[1].join(
            ('<meta property="file-as" refines="#create">明日✿咲葉</meta>\n<dc:subject>lightnovel</dc:subject>\n<dc:rights>voidlord</dc:rights>\n<dc:language>zh</dc:language>\n<meta property="ibooks:specified-fonts">true</meta>\n<meta property="ibooks:binding">true</meta>\n<dc:identifier id="duokan-book-id">none</dc:identifier>\n<meta property="opf:scheme" refines="#duokan-book-id">DKID</meta>\n<dc:identifier id="zhangyue-book-id">none</dc:identifier>\n<meta property="opf:scheme" refines="#zhangyue-book-id">ZYID</meta>\n<meta name="cover" content="', '"/>')))).join(('\n<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:opf="http://www.idpf.org/2007/opf">\n', '\n</metadata>\n'))), bk.setpackagetag('<package version="3.0" unique-identifier="BookId" prefix="rendition: http://www.idpf.org/vocab/rendition/#" xmlns="http://www.idpf.org/2007/opf">'), bk.setspine_ppd('ltr')
        navid, cttid = None, gettype(bk, 'toc')
        for i in bk.manifest_epub3_iter():
            if i[3] == 'nav':
                navid = i[0]
            elif i[2].endswith('xhtml+xml'):
                bk.set_manifest_epub3_attributes(i[0], 'scripted')
            elif i[0] == cover[1]:
                bk.set_manifest_epub3_attributes(i[0], 'cover-image')
            else:
                bk.set_manifest_epub3_attributes(i[0], None)
        spine, linear, prop, line = [i[0] for i in bk.getspine()], [], [], {
            cover[0]: 0, titid: 1, mesid: 2, sumid: 3, navid: 1000000}
        for i, _ in bk.text_iter():
            if i not in line:
                if i in spine:
                    line[i] = (spine.index(i)+1)*1000
                elif i == cttid:
                    spine.append(i)
                    line[cttid] = 4
                else:
                    spine.append(i)
                    s = i.rsplit('_part', 1)
                    line[i] = (spine.index(s[0])+1)*1000+int(s[1])
            elif i not in spine:
                spine.append(i)
        spine.sort(key=lambda x: line[x])
        for i in spine:
            if i:
                linear.append('no') if i == navid else linear.append('yes')
                if i == cover[0]:
                    prop.append('duokan-page-fullscreen')
                elif i in picpg:
                    prop.append('duokan-page-fitwindow')
                else:
                    prop.append(None)
            else:
                spine.remove(i)
        bk.setspine_epub3(tuple(zip(spine, linear, prop)))
        print('　+重构：【', bk.get_opfbookpath(), '】', sep='')
    else:
        print('\n添加XML至META-INF……')
        for i1, i2 in buildxml.items():
            if i1 not in bk._w.other:
                print('　+生成：【', i1, '】', sep='')
                bk.addotherfile(i1, i2)
            else:
                print('　-已存在：【', i1, '】', sep='')
        print('\n添加素材文件……')
        for r, d, f in walk(path.join(bk._w.plugin_dir, bk._w.plugin_name, 'materials')):
            for n in f:
                with open(path.join(r, n), 'rb') as d:
                    build(bk, n, d.read())
        print('\n添加汇总样式表……')
        css = tuple(getbsn(i[1]).join(('@import "', '";'))
                    for i in bk.css_iter())
        build(bk, 'stylesheet.css', '\n'.join(css).join(
            ('/*虚空文学旅团STERAePub++*/\n', '\n/*虚空文学旅团STERAePub++*/'))) if css else print('　-无有效样式表')


def build(bk, bsn, data, mime=None, prop=None):
    mid = bsn
    try:
        bk.addfile(bsn, bsn, data, mime, prop)
        print('　+生成：【', bsn, '】', sep='')
    except:
        try:
            bk.writefile(bsn, data)
        except:
            mid = bk.basename_to_id(bsn)
            bk.writefile(mid, data)
            bsn = getbsn(bk.id_to_href(mid))
        print('　-覆盖：【', bsn, '】', sep='')
    return mid
