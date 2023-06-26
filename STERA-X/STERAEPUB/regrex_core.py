#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from regex import compile, subn
try:
    from .bookenv_core import book
    from .regrex_dict import XH
except ImportError:
    from bookenv_core import book
    from regrex_dict import XH
try:
    from sigil_bs4 import BeautifulSoup
    sigilbs4 = True
except ImportError:
    from bs4 import BeautifulSoup
    sigilbs4 = False

# DOM正则读写
wrap, pginfo, pgsplit = compile(r'(?:\r\n|(?<![\r\n])\r(?![\r\n]))'), compile(
    r'<page href="([^"]*?)">'), compile(r'\s*</page>\s*')


def overwrite(bk: book, bsn: str, data: str | bytes):
    '''
    通过文件名判断文件是否存在，若存在则覆写文件，否则新建文件。\n
    bk -> EPUB的book对象\n
    bsn -> 目标文件的完整文件名\n
    data -> 覆写的文件内容
    '''
    ele = bk.get(bsn=bsn)
    if ele:
        print('　-覆盖：【', ele.write(data).bsn, '】', sep='')
    else:
        ele = bk.set(bk.add(bsn, data))
        print('　+生成：【', ele.bsn, '】', sep='')
    return ele


class dom:
    def __init__(self, bk: book, chk: bool = True):
        '''
        初始化dom对象，将book对象spine中包含的文档使用'<page href="[文件名]">[文档内容]</page>'形式包裹后按顺序连接，并将CRLF统一为LF（\\n）、清除制表符（\\t）。\n
        bk -> EPUB的book对象\n
        chk -> 是否进行样式检查
        '''
        self.bk, self.chk, self.page = bk, chk, '\n'.join(''.join(('<page href="', i.bsn, '">\n', wrap.sub(
            '\n', bs(i.read(), True).expandtabs(1)), '\n</page>')) for i in bk.spine)

    def __call__(self, *flow: bool):
        '''
        调用正则拓展对DOM内容进行查找替换，传入多个参数以确定对应执行组是否执行。\n
        flow -> 是否执行对应次序的查找替换执行组
        '''
        for i in range(len(flow)):
            if flow[i]:
                self.page = reg(self.page, XH[i])
        return self

    def __del__(self):
        '''
        dom对象删除前将已更改内容写入对应文件中，若文件不存在则新建。
        '''
        pgclear = compile(
            r'\s*<page.*?>\s*' if self.chk else r'(?:\s*<page.*?>\s*|\s*type="check")')
        for bsn, data in zip(pginfo.findall(self.page), pgsplit.split(pgclear.sub('', self.page))):
            overwrite(self.bk, bsn, bs(data, True))


def reg(aim: str, regrex: tuple, log: bool = True, debug: bool = False) -> str:
    '''
    二级预查递归正则，将传入的执行组元组的第二项作为预查正则，在其匹配结果中使用正则拓展查找替换，最后返回处理后的文本，查找替换过程根据执行组顺序逐步进行。\n
    aim -> 需处理的原文本\n
    regrex -> 查找替换执行组，是一个第一项为执行组名称、第二项为预查正则、而后若干项为逻辑分组的元组；每一个逻辑分组的第一项是该分组的名称，第二项开始为包含分组内容的一个字典，该字典的每一个键值对中，键是查找内容，值则是对应的替换内容\n
    log -> 是否输出执行组的名称以及每个逻辑分组的名称，与执行组的替换数量\n
    debug -> 是否输出每个键值对的编号与替换数量
    '''
    if log and regrex[0]:
        print('\n', regrex[0], '……', sep='')
    pre = compile(regrex[1].replace('^^', '(?<![^\\n])').replace(
        '$$', '(?![^\\n])')) if regrex[1] else None
    for s in regrex[2:]:
        if debug:
            print('　-【', s[0], '】：', sep='', end='')
        if pre:
            r, pg = 0, [i.group(0) for i in pre.finditer(aim)]
            p = range(len(pg))
            for g in p:
                part = pg[g]
                aim = aim.split(part, 1)
                part, _r = rex(part, s, debug)
                pg[g], aim = ''.join((aim[0], part)), aim[1]
                r += _r
            pg[-1] = ''.join((pg[-1], aim))
            aim = ''.join(pg)
        else:
            aim, r = rex(aim, s, debug)
        if debug:
            print()
        if log:
            print(''.join(('　+替换', str(r), '项：【',
                  s[0], '】') if r else ('　-未匹配到：【', s[0],  '】')))
    return aim


def rex(pg: str, dic: tuple, debug: bool = False):
    '''
    无穷递增正则拓展，返回处理后文本片段与片段的总替换次数，'^'与'$'表示文本整体的开头与结尾，'^^'与'$$'表示一行文本的开头与结尾；在查找正则以'(*)'或'(*[数字])'作为开头的情况下，若没有数字则执行无穷次替换直至文本中不再有匹配结果为止，若有数字则执行数字次数的重复替换；在前述无穷正则修饰符存在条件下，若替换条目中含有'*'，其位置将被替换为以当前已重复次数为基础、前补零的三位数字。\n
    pg -> 需处理的原文本片段\n
    dic -> 查找替换执行组的一个逻辑分组\n
    debug -> 是否输出每个键值对的替换情况
    '''
    ti, step, d = 0, 0, dic[1]
    for m in d:
        if debug:
            step += 1
            print('[', step, '/', len(d), ']', sep='', end='')
        m, r, t = m.replace('^^', '(?<![^\\n])').replace(
            '$$', '(?![^\\n])'), d[m], 0
        if m.startswith('(*'):
            e, x = m.find(')'), 1
            m, n = compile(m[e+1:]), int(m[2:e]) if e > 2 else 0
            while x <= n or not n:
                if m.search(pg):
                    pg, _t = m.subn(r.replace('*', str(x).zfill(3)), pg)
                    t += _t
                    x += 1
                else:
                    break
        else:
            pg, t = subn(m, r, pg)
        ti += t
    return pg, ti


def bs(xt: str, prettify: bool = False) -> BeautifulSoup | str:
    '''
    根据输入的HTML文本返回BeautifulSoup对象或美化后的文本。\n
    xt -> 需处理的HTML文本\n
    prettify -> 是否返回美化后的HTML文本，否则返回BeautifulSoup对象
    '''
    soup = BeautifulSoup(xt, 'lxml')
    return (soup.prettyprint_xhtml() if sigilbs4 else soup.prettify(encoding='unicode')) if prettify else soup
