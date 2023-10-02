#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from regex import compile
from os import path, walk
try:
    from .bookenv_core import book, InvalidEpubError, getbsn, first
    from .regrex_core import bs, reg, overwrite
    from .cpsimg_core import getpic
except ImportError:
    from bookenv_core import book, InvalidEpubError, getbsn, first
    from regrex_core import bs, reg, overwrite
    from cpsimg_core import getpic

# EPUB重构

expg, spanclear, olwrap, tunwrap, tit, bookid = compile(r'(?i)(?:<title></title>|colophon|logo[-_]|bookwalker[^"\n]*?\.)'), compile(r'</?span[^>]*?>'), compile(r'(?s)<ol>\s*(.*?)\s*</ol>$'), compile(
    r'(?:[\n\r]+ *(?=[^< ])|\s*\\?(?= )|\s*(?=</a>))'), compile(r'<dc:title.*?>(.*?)</dc:title>'), compile(r'<dc:identifier.*?id="BookId".*?>(.*?)</dc:identifier>')
fixnav = ('', '', ('', {
          r'</li>((?:\s*<li>\s*<a[^>]*?>　[^<]*?</a>\s*</li>)+)': r'\n<ol>\1\n</ol>\n</li>', r'(<a[^>]*?>)　': r'\1'}))
buildncx = ('', '', ('', {r'<a[^>]*href="[^"]*?([^"/]+)"[^>]*>\s*(.*?)\s*</a>': r'<navLabel>\n<text>\2</text>\n</navLabel>\n<content src="Text/\1"/>',
            r'</li>(?:\s*</ol>)?': '</navPoint>', r'(*)^([\s\S]*?)(?:<ol[^>]*>\s*)?<li[^>]*>': r'\1<navPoint id="navPoint*">'}))
buildxml = {'com.apple.ibooks.display-options.xml': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<display_options>\n<platform name="*">\n<option name="specified-fonts">true</option>\n</platform>\n</display_options>',
            'zhangyue-expansion.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<zhangyue-expansion version="3.4.2">\n<book_id></book_id>\n</zhangyue-expansion>'}


def gettype(bk: book, *etype: str):
    '''
    传入OPF的guide中type属性值，返回包含所有对应elem对象的生成器。\n
    bk -> EPUB的book对象\n
    etype -> 需查询的type属性值
    '''
    t = set(etype)
    for i in etype:
        t.add('other.'+i)
    for i in bk.guide:
        if i.guideType in t:
            yield i


def buildtoc(bk: book, mode: str = 'ncx'):
    '''
    在不同模式下覆盖生成不同位置的目录，默认生成NCX与OPF的guide。\n
    bk -> EPUB的book对象\n
    mode -> 生成模式，'ncx'模式下通过NAV生成NCX与OPF的guide；'ctt'模式下通过NAV生成HTML目录页；'nav'模式下通过NCX生成NAV
    '''
    NAV = bk.nav.read()
    while '>　' in NAV:
        NAV = reg(NAV, fixnav, False)
    NAV = bs(NAV)
    toc, guide = NAV.find('nav', {'epub:type': 'toc'}).ol, NAV.find(
        'nav', {'epub:type': 'landmarks'})
    if mode == 'ctt':
        print('\n生成目录页……')
        for i in toc('li'):
            i.name, i['class'] = 'ctt', 'toc'
            for j in i('ol'):
                j.name, j['class'] = 'ctt', 'part'
        for i in toc('a'):
            if not i.string:
                string = i.getText(strip=True)
                i.clear()
                i.string = string
            i.string.wrap(NAV.new_tag('ch'))
        toc = olwrap.sub(r'<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xml="http://www.w3.org/XML/1998/namespace">\n<head>\n<title>目錄</title>\n<link href="../Styles/stylesheet.css" type="text/css" rel="stylesheet"/>\n<script type="text/javascript" src="../Misc/script.js"></script>\n</head>\n<body>\n<h3 class="ctt">Contents</h3>\n\1\n</body>\n</html>', str(toc))
        try:
            bsn = first(getbsn(guide.find('a', {'epub:type': 'toc'})['href']))
            ele = overwrite(bk, bsn if bsn else 'contents.xhtml', toc)
        except:
            ele = overwrite(bk, 'contents.xhtml', toc)
        ele.guideType, ele.guideTitle = 'toc', '目錄'
        bk.guide = [ele]
        bk.stdopf()
    elif mode == 'nav':
        print('\n重构NAV……')
        cover, ctt, intro = first(getpic(bk)), first(
            gettype(bk, 'toc')), first(gettype(bk, 'introduction'))
        if not cover:
            raise InvalidEpubError('未找到有效的封面图片')
        nav = bs(ctt.read())
        for i in nav.body('p'):
            if i.has_attr('class') and 'ctit' in i['class']:
                i.string = ''.join(('\\ ', i.string))
            i.unwrap()
        for i in nav.body(class_=['toc', 'part']):
            i.name = 'li' if 'toc' in i['class'] else 'ol'
            del i['class']
        bk.nav.write(bs(''.join(('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xml="http://www.w3.org/XML/1998/namespace">\n<head>\n<title>導航</title>\n<link href="../Styles/stylesheet.css" type="text/css" rel="stylesheet"/>\n<script type="text/javascript" src="../Misc/script.js"></script>\n</head>\n<body id="ctt" epub:type="frontmatter" id="nav">\n<nav epub:type="toc" id="toc" role="doc-toc">\n<ol>\n<li><a href="', cover,
                     '">封面</a></li>\n<li><a href="title.xhtml">標題</a></li>\n<li><a href="message.xhtml">製作信息</a></li>', intro.join(('\n<li><a href="', '">簡介</a></li>')) if intro else '', '\n<li><a href="', ctt, '">目錄</a></li>\n', tunwrap.sub('', '\n'.join(str(i) for i in nav.body('li', recursive=False))), '\n</ol>\n</nav>\n<nav epub:type="landmarks" id="landmarks" hidden="">\n<ol>\n<li><a epub:type="cover" href="', cover, '">封面</a></li>', intro.join(('\n<li><a epub:type="introduction" href="', '">簡介</a></li>')) if intro else '', '\n<li><a epub:type="toc" href="', ctt, '">目錄</a></li>\n</ol>\n</nav>\n</body>\n</html>')), True))
        print('　+重构：【', bk.nav.bsn, '】', sep='')
    else:
        depth = {0}

        def _ (soup, level=0):
            if soup:
                level += 1
                for i in soup('li', recursive=False):
                    _(i.ol, level)
            else:
                depth.add(level)
        _(toc)
        depth = max(depth)
        print('\n生成NCX与GUIDE……')
        meta = bk.metadata
        title, bid = tit.search(meta).group(1) if tit.search(
            meta) else '', bookid.search(meta).group(1) if bookid.search(meta) else ''
        bk.guide = []
        for i in guide('a'):
            ele = bk.get(bsn=first(getbsn(i['href'])))
            ele.guideType, ele.guideTitle = i['epub:type'], i.string
            bk.guide.append(ele)
        bk.ncx = overwrite(bk, bk.ncx if bk.ncx else 'toc.ncx', '\n'.join(('<?xml version="1.0" encoding="utf-8"?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n<head>', '<meta name="dtb:uid" content="'+bid + '"/>', '<meta name="dtb:depth" content="' +
                           str(depth) + '"/>', '<meta name="dtb:totalPageCount" content="0"/>\n<meta name="dtb:maxPageNumber" content="0"/>\n</head>\n<docTitle>\n<text>'+title+'</text>\n</docTitle>\n<navMap>', reg(str(toc), buildncx, False), '</navMap>\n</ncx>')))
        bk.stdopf()


def buildtem(bk: book, info: dict = None):
    '''
    根据传入信息构建标准模板，无信息时进行素材导入。\n
    bk -> EPUB的book对象\n
    info -> 包含书籍信息的字典
    '''
    if info:
        print('\n生成信息页……')
        titpg, mespg, sumpg = overwrite(bk, 'title.xhtml', '\n'.join(('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xml="http://www.w3.org/XML/1998/namespace">\n<head>\n<title>標題</title>\n<link href="../Styles/stylesheet.css" type="text/css" rel="stylesheet"/>\n<script type="text/javascript" src="../Misc/script.js"></script>\n</head>\n<body>\n<div class="title">\n<div class="center" style="margin:4em auto 0;">\n<p class="tilh em18 bold">'+info['tit']+'</p>', '<p class="tilh em09 bold" style="margin:1em 0 0;">～'+info['stit']+'～</p>\n</div>' if info['stit'] else '</div>', '<div class="center" style="margin:3em auto 4em;">', '<p class="tilh em15 bold">'+info['vol']+'</p>\n</div>' if info['vol'] else '</div>', '<div class="center">\n<p class="tilh em07 bold">作者</p>\n<p class="tilh em11 bold" style="margin:0.2em 0 0.75em;">'+info['writer']+'</p>\n<p class="tilh em07 bold">插畫</p>\n<p class="tilh bold" style="margin:0.15em 0 0;">'+info['painter']+'</p>\n</div>\n</div>\n</body>\n</html>'))), overwrite(bk, 'message.xhtml', ''.join(
            ('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xml="http://www.w3.org/XML/1998/namespace">\n<head>\n<title>製作信息</title>\n<link href="../Styles/stylesheet.css" type="text/css" rel="stylesheet"/>\n<script type="text/javascript" src="../Misc/script.js"></script>\n</head>\n<body>\n<div class="message">\n<div>\n<div class="meg">\n<p>製 作 信 息</p>\n</div>\n<div class="meghr"/>\n<div class="creator">\n<p>作者</p>\n</div>\n<div>\n<p>', info['writer'], '</p>\n</div>\n<div class="creator">\n<p>插畫</p>\n</div>\n<div>\n<p>', info['painter'], '</p>\n</div>\n<div class="creator">\n<p>譯者</p>\n</div>\n<div>\n<p>', info['translator'], '</p>\n</div>\n<div class="creator">\n<p>圖源</p>\n</div>\n<div>\n<p>', info['introducer'], '</p>\n</div>\n<div class="creator">\n<p>錄入</p>\n</div>\n<div>\n<p>', info['inputer'], '</p>\n</div>\n<div class="group">\n<p><a href="https://www.lightnovel.us">輕之國度錄入組</a>×<a href="https://www.voidlord.com">虛空文學旅團</a></p>\n</div>\n<div class="logo">\n<img alt="logo" src="../Images/logo.png" zy-enlarge-src="none"/>\n</div>\n</div>\n</div>\n</body>\n</html>'))), overwrite(bk, 'summary.xhtml', info['summary'].join(('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xml="http://www.w3.org/XML/1998/namespace">\n<head>\n<title>簡介</title>\n<link href="../Styles/stylesheet.css" type="text/css" rel="stylesheet"/>\n<script type="text/javascript" src="../Misc/script.js"></script>\n</head>\n<body>\n<div class="summary">\n<h3>簡介</h3>\n<hr/>\n', '\n</div>\n</body>\n</html>'))) if info['summary'] else None
        print('\n重构OPF……')
        title, cpg, cover, picpg = ' '.join((info['tit'], info['vol'], info['stit']) if info['stit'] else (
            info['tit'], info['vol'])).strip(), None, None, set()
        for pg, img in getpic(bk):
            if cover:
                picpg.add(pg)
            else:
                cpg, cover = pg, img
        if not cover:
            raise InvalidEpubError('未找到有效的封面图片')
        line, cttpg = {cpg: 0, titpg: 1, mespg: 2,
                       bk.nav: 1000000}, first(gettype(bk, 'toc'))
        if sumpg:
            sumed, line[sumpg], sumpg.guideType, sumpg.guideTitle = first(
                gettype(bk, 'introduction')), 3, 'introduction', '簡介'
            if sumed:
                bk.guide.remove(sumed)
            bk.guide.append(sumpg)
        if cttpg:
            line[cttpg], cttpg.guideTitle = 4, '目錄'
        bk.metadata, bk.ppd = '\n'.join(('<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:opf="http://www.idpf.org/2007/opf">\n<dc:identifier id="BookId">urn:isbn:'+info['isbn']+'</dc:identifier>\n<dc:title id="title">'+title+'</dc:title>', '<meta property="belongs-to-collection" id="num">'+info['tit']+'</meta>\n<meta refines="#num" property="collection-type">series</meta>\n<meta refines="#num" property="group-position">'+info['vol']+'</meta>\n<dc:creator id="create">'+info['writer']+'</dc:creator>\n<dc:contributor>'+info['epuber']+'</dc:contributor>' if info['vol'] else '<dc:contributor>'+info[
                                        'epuber']+'</dc:contributor>', '<meta property="file-as" refines="#create">明日✿咲葉</meta>\n<dc:subject>lightnovel</dc:subject>\n<dc:rights>voidlord</dc:rights>\n<dc:language>zh</dc:language>\n<meta property="ibooks:specified-fonts">true</meta>\n<meta property="ibooks:binding">true</meta>\n<dc:identifier id="duokan-book-id">none</dc:identifier>\n<meta property="opf:scheme" refines="#duokan-book-id">DKID</meta>\n<dc:identifier id="zhangyue-book-id">none</dc:identifier>\n<meta property="opf:scheme" refines="#zhangyue-book-id">ZYID</meta>\n<meta name="cover" content="'+cover.mid+'"/>\n</metadata>')), 'ltr'
        for ele in bk.iter():
            if ele.prop == 'nav':
                if not bk.nav:
                    bk.nav = ele
                elif ele is not bk.nav:
                    ele.prop = 'scripted'
            elif ele.form == 'text':
                ele.prop = 'scripted'
            elif ele is cover:
                ele.prop = 'cover-image'
            else:
                ele.prop = None
        for ele in bk.iter('text'):
            if ele not in bk.spine:
                bk.spine.append(ele)
            if ele not in line:
                try:
                    name, num = ele.rsplit('_part', 1)
                    line[ele] = (bk.spine.index(
                        bk.get(bsn=name))+1)*1000+int(num)
                except:
                    line[ele] = (bk.spine.index(ele)+1)*1000
        bk.spine.sort(key=lambda x: line[x])
        for ele in bk.spine:
            ele.spineLinear = 'no' if ele is bk.nav else 'yes'
            if ele is cpg:
                ele.spineProp = 'duokan-page-fullscreen'
            elif ele in picpg:
                ele.spineProp = 'duokan-page-fitwindow'
            else:
                ele.spineProp = None
        bk.stdopf()
        print('　+重构：【', bk.opf.bsn, '】', sep='')
    else:
        print('\n添加XML至META-INF……')
        for i1, i2 in buildxml.items():
            if not bk.get(bsn=i1):
                print('　+生成：【', i1, '】', sep='')
                bk.add(i1, i2)
            else:
                print('　-已存在：【', i1, '】', sep='')
        print('\n添加素材文件……')
        for r, d, f in walk(path.join(bk.sdir, 'materials')):
            for n in f:
                if 'original' not in n:
                    with open(path.join(r, n), 'rb') as d:
                        overwrite(bk, n, d.read())
        print('\n添加汇总样式表……')
        css = tuple(i.bsn.join(('@import "', '";')) for i in bk.iter('css'))
        overwrite(bk, 'stylesheet.css', '\n'.join(css).join(
            ('/*虚空文学旅团STERAePub++*/\n', '\n/*虚空文学旅团STERAePub++*/'))) if css else print('　-无有效样式表')


def clear(bk: book, mode: str = 'unused'):
    '''
    在不同模式下清理EPUB中不同位置的多余文件，默认清理未使用的媒体文件。
    bk -> EPUB的book对象\n
    mode -> 清理模式，'misc'模式清理与书籍内容无关的杂项文件；'page'模式清理不需要的多余文档页；'unused'模式清理未使用的媒体文件
    '''
    delitem = 0
    if mode == 'misc':
        print('\n清理杂项文件……')
        for ele in bk.iter('css', 'font', 'other', 'misc'):
            if ele.bsn != 'container.xml':
                print('　-删除：【', ele.bsn, '】', sep='')
                bk.delete(ele)
                delitem = 1
    elif mode == 'page':
        print('\n清理多余文档页……')
        for ele in bk.iter('text'):
            if ele is not bk.nav and expg.search(ele.read()):
                print('　-删除：【', ele.bsn, '】', sep='')
                bk.delete(ele)
                delitem = 1
    elif mode == 'unused':
        print('\n清理未使用的文件……')
        UNUSED = {ele for ele in bk.iter(
            'css', 'font', 'audio', 'video', 'misc')}
        for ele in bk.iter('text', 'css'):
            for used in getbsn(ele.read()):
                UNUSED.discard(used)
        for ele in UNUSED:
            print('　-删除：【', ele.bsn, '】', sep='')
            bk.delete(ele)
            delitem = 1
    if not delitem:
        print('　+无多余文件')
