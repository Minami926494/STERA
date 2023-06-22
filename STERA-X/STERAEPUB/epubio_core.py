#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path, makedirs, walk, remove, rename, listdir, rmdir
from shutil import rmtree, copyfile, copytree, move
from zipfile import ZipFile, ZIP_DEFLATED
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
        try:
            with open(self.fp, 'rb') as fp:
                data = fp.read()
        except IsADirectoryError:
            raise IsADirectoryError('文件夹不能作为读取对象')
        except FileNotFoundError:
            raise FileNotFoundError('源路径不存在')
        return data if utf8 else data.decode()

    def write(self, data: str | bytes, clear: bool = False):
        d = path.dirname(self.fp)
        if clear and path.exists(d):
            rmtree(d)
        makedirs(d, exist_ok=True)
        with open(self.fp, 'wb') as fp:
            fp.write(data.encode() if isinstance(data, str) else data)
        return self

    def copy(self, dst: str, clear: bool = False):
        if clear and path.exists(dst):
            self.remove(dst)
        try:
            return elem(copytree(self.fp, dst, dirs_exist_ok=True) if self.isdir else copyfile(self.fp, dst))
        except FileExistsError:
            raise FileExistsError('目标路径存在重名文件')
        except FileNotFoundError:
            raise FileNotFoundError('源路径不存在')

    def move(self, dst: str, clear: bool = False):
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

    def rename(self, nbsn: str):
        dst = pjoin(path.dirname(self.fp), nbsn)
        try:
            rename(self.fp, dst)
            self.__init__(dst)
        except FileExistsError:
            raise FileExistsError('目标路径存在重名文件')
        except FileNotFoundError:
            raise FileNotFoundError('源路径不存在')
        return self

    def extract(self, dst: str, clear: bool = False):
        if not self.fp.lower().endswith('.epub'):
            raise InvalidEpubError('不是有效的EPUB文件')
        elif clear and path.exists(dst):
            self.remove(dst)
        with ZipFile(self.fp) as zip:
            zip.extractall(dst)
        return elem(dst)

    def create(self, dst: str, clear: bool = False):
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
        fp = self.fp
        try:
            if self.isdir:
                rmtree(fp)
            else:
                remove(fp)
                dclear(fp)
        except FileNotFoundError:
            raise FileNotFoundError('源路径不存在')
