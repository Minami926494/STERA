#!/usr/bin/env python
# -*- coding: utf-8 -*-
from re import compile, subn
from .regrex_dict import XH
from .clear_core import getbsn
try:
    from sigil_bs4 import BeautifulSoup
except:
    from bs4 import BeautifulSoup

# DOM正则读写
wrap, pginfo, pgsplit = compile(r'(?:\r\n|(?<![\r\n])\r(?![\r\n]))'), compile(
    r'<page id="(.*?)" href="(.*?)">'), compile(r'\s*</page>\s*')


def bs(xt, prettify=False):
    if prettify:
        try:
            return BeautifulSoup(xt, 'lxml').prettyprint_xhtml()
        except:
            return BeautifulSoup(xt, 'lxml').prettify(encoding='utf-8')
    else:
        return BeautifulSoup(xt, 'lxml')


class dom:
    def __init__(self, bk, chk=True):
        self.bk, self.chk, self.id, self.page = bk, chk, (i[0] for i in bk.text_iter()), '\n'.join((''.join(('<page id="', i[0], '" href="', getbsn(
            i[1]), '">\n', wrap.sub('\n', bs(bk.readfile(i[0]), True).expandtabs(1)), '\n</page>')) for i in bk.text_iter()))

    def __call__(self, *flow):
        for i in range(len(flow)):
            if flow[i]:
                self.page = reg(self.page, XH[i])
        return self

    def __del__(self):
        pgclear = compile(
            r'\s*<page.*?>\s*') if self.chk else compile(r'(?:\s*<page.*?>\s*|\s*type="check")')
        pgs = zip(pginfo.findall(self.page),
                  pgsplit.split(pgclear.sub('', self.page)))
        for (id, bsn), data in pgs:
            self.bk.writefile(id, bs(data, True)) if id in self.id else self.bk.addfile(id, bsn, bs(data, True))


def reg(aim, regrex, log=True):
    if log and regrex[0]:
        print('\n', regrex[0], '……', sep='')
    pre = compile(regrex[1].replace('^^', '(?<![^\\n])').replace(
        '$$', '(?![^\\n])')) if regrex[1] else None
    for s in regrex[2:]:
        if pre:
            r, pg = 0, [i.group(0) for i in pre.finditer(aim)]
            p = range(len(pg))
            for g in p:
                part = pg[g]
                aim = aim.split(part, 1)
                part, _r = rex(part, s)
                pg[g], aim = ''.join((aim[0], part)), aim[1]
                r += _r
            pg[-1] = ''.join((pg[-1], aim))
            aim = ''.join(pg)
        else:
            aim, r = rex(aim, s)
        if log:
            print(''.join(('　+替换', str(r), '项：【',
                  s[0], '】') if r else ('　-未匹配到：【', s[0],  '】')))
    return aim


def rex(pg, dic):
    ti, d = 0, dic[1]
    for m in d:
        m, r, t = m.replace('^^', '(?<![^\\n])').replace(
            '$$', '(?![^\\n])'), d[m], 0
        if m.startswith('(*'):
            e, x = m.find(')'), 1
            m, n = compile(m[e+1:]), int(m[2:e]) if e > 2 else 0
            while x <= n or not n:
                pg, _t = m.subn(r.replace('*', str(x).zfill(3)), pg)
                if _t:
                    t += _t
                    x += 1
                else:
                    break
        else:
            pg, t = subn(m, r, pg)
        ti += t
    return pg, ti
