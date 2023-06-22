#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from regex import compile, sub, Match
from lxml.etree import fromstring, tostring
from os import path, walk
from time import time
from html import unescape
from copy import copy
from types import MethodType
from collections.abc import Generator
try:
    from .epubio_core import pjoin, elem, InvalidEpubError
    from .epubio_dict import extinfo
except ImportError:
    from epubio_core import pjoin, elem, InvalidEpubError
    from epubio_dict import extinfo

# EPUB解析
linkpath, navmap, ol1, ol2, navpoint, navlabel = compile(r'(?<=url\(|url\([\'\"]|href=[\'\"]|[^-]src=[\'\"]|@import [\'\"])[^)\'\"#:]+?(?=[)\'\"#])'), compile(r'(?i)[\s\S]*<navMap>([\s\S]*)</navMap>[\s\S]*'), compile(
    r'</li>\s*(?=</li>)'), compile(r'(<li>(?:(?!</li>)[\s\S])*?)(?=<li>)'), compile(r'(?i)<(/)?navPoint[^>]*?>'), compile(r'(?i)<navLabel[^>]*?>\s*<text[^>]*?>([^<]*?)</text>\s*</navLabel>\s*<content[^>]*?src="[^"]*?([^"/]+)"[^>]*?/>')


def extlower(bsn: str) -> str:
    '''
    将文件名的扩展名转换为小写后返回完整文件名。\n
    bsn -> 原完整文件名
    '''
    name, ext = path.splitext(bsn)
    return name+ext.lower()


class book:
    def __init__(self, src: str, runInSigil: bool = False):
        '''
        传入源EPUB以初始化book对象并执行规范化，将在系统的用户文件夹下建立工作区。\n
        src -> 源EPUB文件（夹）路径\n
        runInSigil -> 是否在Sigil中作为插件运行
        '''
        self.runInSigil, norepeat = runInSigil, {'container.xml', 'mimetype'}
        outdir = self.outdir = pjoin(path.expanduser('~').replace(
            '\\', '/'), 'STERAEPUB', str(time()).replace('.', '-'))
        oebps = self.oebps = pjoin(outdir, 'OEBPS')
        metainf = self.metainf = pjoin(outdir, 'META-INF')
        stdopfpath, stdncxpath = pjoin(
            oebps, 'content.opf'), pjoin(oebps, 'toc.ncx')
        opfpath = ncxpath = None
        elem(src).copy(outdir, True) if runInSigil == 'sigil' else elem(
            src).extract(outdir, True)
        elems = self.elems = {elem(pjoin(metainf, 'container.xml')).write(
            '<?xml version="1.0" encoding="UTF-8"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n<rootfiles>\n<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n</rootfiles>\n</container>'), elem(pjoin(outdir, 'mimetype')).write('application/epub+zip')}
        mid2ele = self.mid2ele = {}
        href2ele = self.href2ele = {}
        fp2ele = self.fp2ele = {}
        bsn2ele = self.bsn2ele = {}
        for r, d, f in walk(outdir):
            for n in f:
                ele, stdpath = elem(pjoin(r, n)), None
                fp, ext, group = ele.fp, ele.ext, ele.group
                if ext != ext.lower():
                    n = extlower(n)
                    ele.rename(n)
                if n in norepeat:
                    continue
                elif group:
                    stdpath = pjoin(metainf, ele.bsn) if ele.form == 'other' else pjoin(
                        oebps, group, ele.bsn)
                elif ext == '.opf' and not opfpath:
                    stdpath = opfpath = stdopfpath
                elif ext == '.ncx' and not ncxpath:
                    stdpath = ncxpath = stdncxpath
                if not stdpath:
                    ele.remove()
                    continue
                elif fp != stdpath:
                    ele.move(stdpath)
                elems.add(ele)
                norepeat.add(n)
                fp2ele[stdpath], bsn2ele[n] = ele, ele
                if ele.href:
                    href2ele[ele.href] = ele
        if not opfpath:
            raise InvalidEpubError('未找到有效的OPF')
        opf = self.opf = fp2ele[opfpath]
        opftree, self.ncx, self.nav = fromstring(
            opf.read(True)), fp2ele.get(ncxpath), None
        ns = {'ns': 'http://www.idpf.org/2007/opf'}
        for item in opftree.xpath('//ns:item[@id and @href]', namespaces=ns):
            mid, href, prop = item.get('id'), item.get(
                'href'), item.get('properties')
            ele = bsn2ele.get(extlower(path.basename(href)))
            if ele:
                ele.mid, ele.prop = mid, prop if prop else None
                if prop == 'nav':
                    if self.nav:
                        prop = None
                    else:
                        self.nav = ele
                mid2ele[mid] = ele
        spine = self.spine = []
        for itemref in opftree.xpath('//ns:itemref[@idref]', namespaces=ns):
            idref, linear, prop = itemref.get('idref'), itemref.get(
                'linear'), itemref.get('properties')
            ele = mid2ele.get(idref)
            if ele:
                ele.spineLinear, ele.spineProp = linear if linear else None, prop if prop else None
                spine.append(ele)
        for ele in self.iter('text'):
            if ele not in spine:
                spine.append(ele)
        guide = self.guide = []
        for reference in opftree.xpath('//ns:reference[@href and @type and @title]', namespaces=ns):
            href, type_, title = reference.get(
                'href'), reference.get('type'), itemref.get('title')
            ele = self.get(bsn=extlower(path.basename(href)))
            if ele:
                ele.guideType, ele.guideTitle = type_, title if title else ''
                guide.append(ele)
        stdmeta = '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:opf="http://www.idpf.org/2007/opf">'
        for meta in opftree.xpath('//ns:metadata', namespaces=ns):
            self.metadata = sub(
                r'<metadata[^>]*?>', stdmeta, unescape(tostring(meta, encoding='unicode')))
            break
        else:
            self.metadata = stdmeta+'\n</metadata>'
        for sp in opftree.xpath('//ns:spine', namespaces=ns):
            ppd = sp.get('page-progression-direction')
            self.ppd = ppd if ppd == 'ltr' or ppd == 'rtl' else None
            break
        else:
            self.ppd = None
        self.ref('text', 'css', 'ncx').stdopf(
        ) if self.nav else self.newnav(False)

    def get(self, mid: str | None = None, href:  str | None = None, fp:  str | None = None, bsn:  str | None = None) -> elem | None:
        '''
        通过对应的参数返回元素对应的elem对象，填入多个参数时按下述顺序查找直至有返回结果。\n
        mid -> 文件对应的manifest id\n
        href -> 文件在OPF中的href\n
        fp -> 文件的绝对路径\n
        bsn -> 文件的完整文件名
        '''
        if mid and mid in self.mid2ele:
            return self.mid2ele[mid]
        elif href and href in self.href2ele:
            return self.href2ele[href]
        elif fp and fp in self.fp2ele:
            return self.fp2ele[fp]
        elif bsn and bsn in self.bsn2ele:
            return self.bsn2ele[bsn]

    def iter(self, *form: str) -> Generator[elem] | None:
        '''
        通过类型参数返回包含所有该类型文件elem对象的迭代器，多个参数时可匹配多类型文件。\n
        form -> 文件类型参数（'text'：HTML类文档 | 'css'：CSS样式表 | 'font'：字体文件 | 'audio'：音频文件 | 'video'：视频文件 | 'ncx'：NCX文件 | 'other'：META-INF中的XML文件 | 'misc'：其他常见类型文件）
        '''
        for ele in copy(self.elems):
            if ele.form in form:
                yield ele

    def add(self, bsn: str, data: str | bytes):
        '''
        通过新文件的完整文件名和文件内容向EPUB添加文件并根据文件类型决定是否添加OPF条目（manifest和spine），重名时将自动重命名，返回新文件的elem对象。\n
        bsn -> 新文件的完整文件名\n
        data -> 新文件的文件内容
        '''
        name, ext = path.splitext(bsn)
        ext = ext.lower()
        bsn = name+ext
        while bsn in self.bsn2ele:
            name += '_'
            bsn = name+ext
        fp = pjoin(self.oebps, extinfo[ext], bsn) if ext in extinfo else pjoin(
            self.metainf, bsn)
        new = elem(fp).write(data)
        self.fp2ele[fp], self.bsn2ele[bsn] = new, new
        self.elems.add(new)
        return new

    def set(self, ele: elem, prop: str | None = None, spineLinear: str | None = None, spineProp: str | None = None, guideType: str | None = None, guideTitle: str | None = None):
        '''
        设置elem对象对应文件在OPF中的各属性值，无传入值时对应属性不作处理，相应属性或包含属性的条目（manifest、spine和guide）不在OPF中则自动新建，返回处理后的elem对象。\n
        ele -> 文件的elem对象\n
        prop -> 文件在manifest中的properties属性值\n
        spineLinear -> 文件在spine中的linear属性值\n
        spineProp -> 文件在spine中的properties属性值\n
        guideType -> 文件在guide中的type属性值\n
        guideTitle -> 文件在guide中的title属性值
        '''
        if ele.group is None:
            raise InvalidEpubError('不支持的文件类型')
        state = 0
        if not ele.mid:
            mid, state = ele.bsn, 1
            while mid in self.mid2ele:
                mid += '_'
            ele.mid = mid
            self.mid2ele[mid], self.href2ele[ele.href] = ele, ele
        if prop:
            ele.prop, state = prop, 1
        if spineLinear:
            ele.spineLinear, state = spineLinear, 1
        if spineProp:
            ele.spineProp, state = spineProp, 1
        if ele not in self.spine and (ele.form == 'text' or spineLinear or spineProp):
            state = 1
            self.spine.append(ele)
        if guideType:
            ele.guideType, state = guideType, 1
        if guideTitle:
            ele.guideTitle, state = guideTitle, 1
        if ele not in self.guide and (guideType or guideTitle):
            state = 1
            self.guide.append(ele)
        if state:
            self.stdopf()
        return ele

    def delete(self, ele: elem, delfile: bool = True):
        '''
        将elem对象对应的文件从EPUB中删除，移除其OPF条目（manifest和spine，如果存在），返回被删除文件的elem对象（如果存在）。\n
        ele -> 文件的elem对象\n
        delfile -> 是否删除文件本身
        '''
        mid = self.mid2ele.pop(ele.mid, None)
        self.href2ele.pop(ele.href, None)
        self.fp2ele.pop(ele.fp, None)
        self.bsn2ele.pop(ele.bsn, None)
        self.elems.discard(ele)
        if mid:
            if ele in self.spine:
                self.spine.remove(mid)
            if ele in self.guide:
                self.guide.remove(mid)
            self.stdopf()
        return ele.remove() if delfile else ele

    def ref(self, *form: str):
        '''
        重定向类型参数所对应文件内容中存在的无效超链接地址，返回book对象，多个参数时可匹配多类型文件。\n
        form -> 文件类型参数（'text'：HTML类文档 | 'css'：CSS样式表 | 'font'：字体文件 | 'audio'：音频文件 | 'video'：视频文件 | 'ncx'：NCX文件 | 'other'：META-INF中的XML文件 | 'misc'：其他常见类型文件）
        '''
        for ele in self.iter(*form):
            data = ele.read()
            if linkpath.search(data):
                ele.write(linkpath.sub(
                    lambda x: self.__ref(x, ele.form), data))
        return self

    def __ref(self, match: Match[str], form: str) -> str:
        match = match.group(0)
        ele = self.bsn2ele.get(path.basename(match))
        if not ele:
            return match
        elif form == 'ncx':
            return ele.href
        elif ele.form == form:
            return ele.bsn
        else:
            return '../'+ele.href

    def newnav(self, cover: bool = True) -> elem:
        '''
        通过NCX生成新的NAV，返回新NAV的elem对象。\n
        cover -> 是否覆盖已存在的NAV
        '''
        if not self.ncx:
            raise InvalidEpubError('未找到有效的NCX')
        newnav = navmap.sub(lambda x: '\n'.join(('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xml="http://www.w3.org/XML/1998/namespace">\n<head>\n<title>導航</title>\n<link href="../Styles/stylesheet.css" type="text/css" rel="stylesheet"/>\n<script type="text/javascript" src="../Misc/script.js"></script>\n</head>\n<body epub:type="frontmatter" id="nav">\n<nav epub:type="toc" id="toc" role="doc-toc">\n<ol>',
                            x.group(1), '</ol>\n</nav>\n<nav epub:type="landmarks" id="landmarks" hidden="">\n<ol>', *('<li><a epub:type="'+ele.guideType+'" href="'+ele.href+'">'+ele.guideTitle+'</a></li>' for ele in self.guide), '</ol>\n</nav>\n</body>\n</html>')), ol1.sub('</li>\n</ol>', ol2.sub(r'\1\n<ol>', navpoint.sub(r'<\1li>', navlabel.sub(r'<a href="\2">\1</a>', self.ncx.read())))))
        if not self.nav:
            self.nav = self.add('nav.xhtml', newnav)
        elif cover:
            self.nav.write(newnav)
        return self.ref('text', 'css', 'ncx').nav

    def stdopf(self) -> elem:
        '''
        生成新的OPF并覆盖旧的OPF，返回OPF的elem对象。
        '''
        return self.opf.write('\n'.join(('<?xml version="1.0" encoding="utf-8"?>\n<package version="3.0" unique-identifier="BookId" prefix="rendition: http://www.idpf.org/vocab/rendition/#" xmlns="http://www.idpf.org/2007/opf">', self.metadata, *('<item id="%s" href="%s" media-type="%s"/>' % (mid, ele.href, ele.mime+'" properties="'+ele.prop if ele.prop else ele.mime) for mid, ele in self.mid2ele.items()), '<spine%s%s>' % (' page-progression-direction="'+self.ppd+'"' if self.ppd else '', ' toc="'+self.ncx.mid+'"' if self.ncx else ''), *('<itemref idref="%s"%s%s/>' % (ele.mid, ' linear="'+ele.spineLinear+'"' if ele.spineLinear else '', ' properties="'+ele.spineProp+'"' if ele.spineProp else '') for ele in self.spine), '</spine>\n<guide>', *('<reference type="'+ele.guideType+'" title="'+ele.guideTitle+'" href="'+ele.href+'"/>' for ele in self.guide), '</guide>\n</package>')))

    def save(self, dst: str, done: bool = False):
        '''
        将工作区中内容保存并输出为EPUB文件，返回book对象（如果存在）。\n
        dst -> EPUB文件输出路径\n
        done -> 是否已经完成处理，若完成将删除工作区和book对象
        '''
        outdir = elem(self.outdir)
        outdir.create(dst, True)
        if not done:
            return self
        outdir.remove()
        del self
