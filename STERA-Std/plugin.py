#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path, makedirs, walk
from shutil import rmtree
from regex import compile, sub
from zipfile import ZipFile, ZIP_DEFLATED
from sys import exit

linkpath = compile(
    r'(?<=url\(|href=|[^-]src=|@import )[\'\"][^\'\":]*?([^\'\"/#:.]+?)(\.[A-z\d]+)(#[^\'\"]*?)?[\'\"]')
m2g = {'image/jpeg': 'Images',
       'image/png': 'Images',
       'image/gif': 'Images',
       'image/svg+xml': 'Images',
       'image/bmp': 'Images',
       'image/tiff': 'Images',
       'image/webp': 'Images',
       'text/html': 'Text',
       'application/xhtml+xml': 'Text',
       'application/x-dtbook+xml': 'Text',
       'font/woff2': 'Fonts',
       'font/woff': 'Fonts',
       'font/ttf': 'Fonts',
       'font/otf': 'Fonts',
       'font/sfnt': 'Fonts',
       'font/collection': 'Fonts',
       'application/vnd.ms-opentype': 'Fonts',
       'application/font-sfnt': 'Fonts',
       'application/font-ttf': 'Fonts',
       'application/font-otf': 'Fonts',
       'application/font-woff': 'Fonts',
       'application/font-woff2': 'Fonts',
       'application/x-font-ttf': 'Fonts',
       'application/x-truetype-font': 'Fonts',
       'application/x-opentype-font': 'Fonts',
       'application/x-font-ttf': 'Fonts',
       'application/x-font-otf': 'Fonts',
       'application/x-font-opentype': 'Fonts',
       'application/x-font-truetype': 'Fonts',
       'application/x-font-truetype-collection': 'Fonts',
       'audio/mpeg': 'Audio',
       'audio/mp3': 'Audio',
       'audio/mp4': 'Audio',
       'audio/ogg': 'Audio',
       'video/mp4': 'Video',
       'video/ogg': 'Video',
       'video/webm': 'Video',
       'text/vtt': 'Video',
       'application/ttml+xml': 'Video',
       'text/css': 'Styles',
       'application/oebps-page-map+xml': 'Misc',
       'application/vnd.adobe-page-map+xml': 'Misc',
       'application/vnd.adobe.page-map+xml': 'Misc',
       'application/smil+xml': 'Misc',
       'application/adobe-page-template+xml': 'Misc',
       'application/vnd.adobe-page-template+xml': 'Misc',
       'text/javascript': 'Misc',
       'application/javascript': 'Misc',
       'application/pls+xml': 'Misc',
       'text/plain': 'Misc'}
f2m = {'.bm': 'image/bmp',
       '.bmp': 'image/bmp',
       '.css': 'text/css',
       '.gif': 'image/gif',
       '.htm': 'application/xhtml+xml',
       '.html': 'application/xhtml+xml',
       '.jpeg': 'image/jpeg',
       '.jpg': 'image/jpeg',
       '.js': 'application/javascript',
       '.m4a': 'audio/mp4',
       '.m4v': 'video/mp4',
       '.mp3': 'audio/mpeg',
       '.mp4': 'video/mp4',
       '.oga': 'audio/ogg',
       '.ogg': 'audio/ogg',
       '.ogv': 'video/ogg',
       '.otf': 'font/otf',
       '.pls': 'application/pls+xml',
       '.png': 'image/png',
       '.smil': 'application/smil+xml',
       '.svg': 'image/svg+xml',
       '.tif': 'image/tiff',
       '.tiff': 'image/tiff',
       '.ttc': 'font/collection',
       '.ttf': 'font/ttf',
       '.ttml': 'application/ttml+xml',
       '.txt': 'text/plain',
       '.vtt': 'text/vtt',
       '.webm': 'video/webm',
       '.webp': 'image/webp',
       '.woff': 'font/woff',
       '.woff2': 'font/woff2',
       '.xhtml': 'application/xhtml+xml',
       '.xml': 'application/oebps-page-map+xml',
       '.xpgt': 'application/vnd.adobe-page-template+xml'}


def writefile(fp, inner):
    d = path.dirname(fp)
    if not path.exists(d):
        makedirs(d)
    with open(fp, 'wb') as fp:
        fp.write(inner.encode() if isinstance(inner, str) else inner)


def run(bk):
    outdir, ncxid, manifest = path.join(
        bk._w.plugin_dir, bk._w.plugin_name, '__stdtmp__'), bk._w.gettocid(), []
    tdir, edir = path.join(outdir, 'tmp'), path.join(outdir, 'tmp.epub')
    if path.exists(tdir):
        rmtree(tdir)
    writefile(path.join(tdir, 'META-INF', 'container.xml'), '<?xml version="1.0" encoding="UTF-8"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n<rootfiles>\n<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n</rootfiles>\n</container>')
    writefile(path.join(tdir, 'mimetype'), 'application/epub+zip')
    if not bk._w.getnavid():
        name, toc = 'nav', sub(r'(?i)[\s\S]*<navMap>([\s\S]*)</navMap>[\s\S]*', lambda x: ''.join(('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xml="http://www.w3.org/XML/1998/namespace">\n<head>\n<title>導航</title>\n<link href="../Styles/stylesheet.css" type="text/css" rel="stylesheet"/>\n<script type="text/javascript" src="../Misc/script.js"></script>\n</head>\n<body epub:type="frontmatter" id="nav">\n<nav epub:type="toc" id="toc" role="doc-toc">\n<ol>',
                               x.group(1), '</ol>\n</nav>\n<nav epub:type="landmarks" id="landmarks" hidden="">\n<ol>\n', '\n'.join(''.join(('<li><a epub:type="', i[0], '" href="', i[2], '">', i[1], '</a></li>')) for i in bk._w.guide), '\n</ol>\n</nav>\n</body>\n</html>')), sub(r'</li>\s*(?=</li>)', r'</li>\n</ol>', sub(r'(<li>(?:(?!</li>)[\s\S])*?)(?=<li>)', r'\1\n<ol>', sub(r'(?i)<(/)?navPoint[^>]*?>', r'<\1li>', sub(r'(?i)<navLabel[^>]*?>\s*<text[^>]*?>([^<]*?)</text>\s*</navLabel>\s*<content[^>]*?src="[^"]*?([^"/]+)"[^>]*?/>', r'<a href="\2">\1</a>', bk._w.readfile(bk._w.gettocid()))))))
        while 1:
            try:
                bk._w.addfile(name, ''.join((name, '.xhtml')),
                              toc, properties='nav')
                bk._w.spine_insert_before(-1, name, 'no')
                break
            except:
                name += '_'
    for id, mime in bk._w.id_to_mime.items():
        if not bk._w.id_to_filepath.get(id):
            continue
        elif id == ncxid:
            bsn = bk._w.id_to_href[id].rsplit('/', 1)[-1]
            manifest.append(''.join(('<item id="', id, '" href="',
                            bsn, '" media-type="application/x-dtbncx+xml"/>')))
            writefile(path.join(tdir, 'OEBPS', bsn), bk._w.readfile(id))
        else:
            (n, f), group, prop = bk._w.id_to_href[id].rsplit(
                '/', 1)[-1].rsplit('.', 1), m2g.get(mime), bk._w.id_to_props.get(id)
            f = ''.join(('.', f.lower()))
            bsn = ''.join((n, f))
            if group:
                manifest.append(''.join(('<item id="', id, '" href="', group, '/', bsn,
                                '" media-type="', mime, ''.join(('" properties="', prop)) if prop else '', '"/>')))
            elif f in f2m:
                manifest.append(''.join(('<item id="', id, '" href="', m2g[f2m[f]], '/', bsn, '" media-type="', f2m[f], ''.join(
                    ('" properties="', prop)) if prop else '', '"/>')))
            else:
                continue
            writefile(path.join(tdir, 'OEBPS', group, bsn), linkpath.sub(lambda x: ''.join(('"../', m2g[f2m[x.group(2).lower()]], '/', x.group(1), x.group(
                2).lower(), x.group(3) if x.group(3) else '', '"')), bk._w.readfile(id)) if mime.endswith(('xml', 'css')) else bk._w.readfile(id))
    for i in bk._w.other:
        if 'container.xml' not in i and i.endswith('.xml'):
            writefile(path.join(tdir, 'META-INF', i.rsplit('/', 1)
                      [-1]), bk._w.readotherfile(i))
    writefile(path.join(tdir, 'OEBPS', 'content.opf'), sub(r'<package[^>]*?>', '<package version="3.0" unique-identifier="BookId" prefix="rendition: http://www.idpf.org/vocab/rendition/#" xmlns="http://www.idpf.org/2007/opf">', sub(r'(?<=<manifest>)[\s\S]+?(?=</manifest>)', '\n'.join(
        manifest), linkpath.sub(lambda x: x.group(1).join(('"', '.ncx"')) if x.group(2).lower() == '.ncx' else ''.join(('"', m2g[f2m[x.group(2).lower()]], '/',  x.group(1), x.group(2).lower(), x.group(3) if x.group(3) else '', '"')), bk._w.build_opf()))))
    with ZipFile(edir, 'w', ZIP_DEFLATED) as zip:
        for r, d, f in walk(tdir):
            for n in f:
                absdir = path.join(r, n)
                with open(absdir, 'rb') as fp:
                    zip.writestr(path.relpath(absdir, tdir),
                                 fp.read(), ZIP_DEFLATED)
    with open(edir, 'rb') as e:
        bk.addotherfile(path.basename(bk._w.epub_filepath), e.read())
    rmtree(outdir)
    return 0


if __name__ == '__main__':
    print('程序运行环境异常！')
    exit(-1)
