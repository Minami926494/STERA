#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path, makedirs, walk, remove, rename, listdir, rmdir
from shutil import rmtree, copyfile, copytree, move
from zipfile import ZipFile, ZIP_DEFLATED
try:
    from .epubio_dict import extinfo
except ImportError:
    from epubio_dict import extinfo


# 基础文件读写
def pjoin(*p: str):
    return '/'.join(p)


def dclear(fp):
    fp = path.dirname(fp)
    if not listdir(fp):
        rmdir(fp)
        dclear(fp)


class InvalidEpubError(Exception):
    pass


class elem:
    def __init__(self, fp: str):
        '''
        传入文件路径，初始化elem对象。\n
        fp -> 文件的完整路径
        '''
        self.fp = fp.replace('\\', '/')
        bsn = self.bsn = path.basename(fp)
        isdir = self.isdir = path.isdir(fp)
        if not isdir:
            self.name, self.ext = path.splitext(bsn)
            self.mid = self.href = self.prop = self.mime = self.form = self.group = self.spineLinear = self.spineProp = self.guideType = self.guideTitle = None
            if '.' in bsn:
                ext = self.ext.lower()
                if ext in extinfo:
                    self.mime, self.form, self.group = extinfo[ext]
                    self.href = pjoin(self.group, bsn)
                elif ext == 'xml':
                    self.form = 'other'

    def read(self, utf8: bool = False):
        '''
        读取并返回elem对象的文件内容。\n
        utf8 -> 是否返回UTF-8，否则返回Unicode
        '''
        try:
            with open(self.fp, 'rb') as fp:
                data = fp.read()
        except IsADirectoryError:
            raise IsADirectoryError('文件夹不能作为读取对象')
        except FileNotFoundError:
            raise FileNotFoundError('源路径不存在')
        return data if utf8 else data.decode()

    def write(self, data: str | bytes):
        '''
        写入elem对象的文件内容，返回elem对象，将自动创建路径中不存在的文件夹。\n
        data -> 写入的字符串或字节序列
        '''
        makedirs(path.dirname(self.fp), exist_ok=True)
        with open(self.fp, 'wb') as fp:
            fp.write(data.encode() if isinstance(data, str) else data)
        return self

    def copy(self, dst: str, clear: bool = False):
        '''
        复制elem对象对应文件到目标路径，返回复制后的新elem对象，将自动创建路径中不存在的文件夹。\n
        dst -> 复制的目标路径\n
        clear -> 是否删除目标路径中已存在的文件（夹）
        '''
        if clear and path.exists(dst):
            self.remove(dst)
        makedirs(path.dirname(dst), exist_ok=True)
        try:
            return elem(copytree(self.fp, dst, dirs_exist_ok=True) if self.isdir else copyfile(self.fp, dst))
        except FileExistsError:
            raise FileExistsError('目标路径存在重名文件')
        except FileNotFoundError:
            raise FileNotFoundError('源路径不存在')

    def move(self, dst: str, clear: bool = False):
        '''
        移动elem对象的文件到目标路径，返回elem对象，将自动创建路径中不存在的文件夹。\n
        dst -> 移动的目标路径\n
        clear -> 是否删除目标路径中已存在的文件（夹）
        '''
        if clear and path.exists(dst):
            self.remove(dst)
        makedirs(path.dirname(dst), exist_ok=True)
        fp = self.fp
        try:
            self.__init__(move(fp, dst))
        except FileExistsError:
            raise FileExistsError('目标路径存在重名文件')
        except FileNotFoundError:
            raise FileNotFoundError('源路径不存在')
        dclear(fp)
        return self

    def rename(self, nbsn: str, clear: bool = False):
        '''
        重命名elem对象对应文件，返回elem对象。\n
        nbsn -> 新的完整文件名\n
        clear -> 是否删除重名的文件（夹）
        '''
        dst = pjoin(path.dirname(self.fp), nbsn)
        if clear and path.exists(dst):
            self.remove(dst)
        try:
            rename(self.fp, dst)
            self.__init__(dst)
        except FileExistsError:
            raise FileExistsError('目标路径存在重名文件')
        except FileNotFoundError:
            raise FileNotFoundError('源路径不存在')
        return self

    def extract(self, dst: str, clear: bool = False):
        '''
        解压EPUB文件到目标路径，返回解压后目录对应的elem对象。\n
        dst -> 解压的目标路径\n
        clear -> 是否删除目标路径中已存在的文件（夹）
        '''
        if not self.fp.lower().endswith('.epub'):
            raise InvalidEpubError('不是有效的EPUB文件')
        elif clear and path.exists(dst):
            self.remove(dst)
        with ZipFile(self.fp) as zip:
            zip.extractall(dst)
        return elem(dst)

    def create(self, dst: str, clear: bool = False):
        '''
        压缩文件夹并生成EPUB文件到目标路径，返回EPUB文件的elem对象。\n
        dst -> 压缩的目标路径\n
        clear -> 是否删除目标路径中已存在的文件（夹）
        '''
        if not dst.lower().endswith('.epub'):
            raise InvalidEpubError('不是有效的EPUB文件')
        elif clear and path.exists(dst):
            self.remove(dst)
        with ZipFile(dst, 'w', ZIP_DEFLATED) as zip:
            for r, d, f in walk(self.fp):
                for n in f:
                    absdir = pjoin(r, n)
                    with open(absdir, 'rb') as fp:
                        zip.writestr(path.relpath(absdir, self.fp),
                                     fp.read(), ZIP_DEFLATED)
        return elem(dst)

    def remove(self):
        '''
        删除elem对象及对应的文件，递归清除删除产生的空文件夹。
        '''
        fp = self.fp
        try:
            if self.isdir:
                rmtree(fp)
            else:
                remove(fp)
                dclear(fp)
        except FileNotFoundError:
            raise FileNotFoundError('源路径不存在')
