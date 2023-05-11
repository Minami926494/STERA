#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from re import compile
from os import path, startfile, remove
from sys import argv
from json import loads, dumps
from .userpanel_ui import Ui_panel

# 用户面板UI
f2p, gettit, getisbn, getsub, getvol, getsum, setsum, chkisbn = compile(r'[ａ-ｚＡ-Ｚ０-９]'), compile(r'<dc:title.*?>\s*([^<>]*?)\s*</dc:title>'), compile(r'(?i)<dc:identifier.*?>[^<>]*?isbn[^<>]*?([\d\s-]+)</dc:identifier>'), compile(
    r'[~～\s](\S*?[^\d\sA-z]\S*?)(?:[~～\s]|$)'), compile(r'([(（【〈-])?(\d+)(?(1)[)）】〉]|(?:\s|$))'), compile(r'(?:^[\s\S]+<body.*?>\s*|\s*</body>[\s\S]+$)|(?<=<p)[^>]+|(?<=<br)[^/]+'), compile(r'<[^>]+>'), compile(r'\D+')


def launch(bk):
    app, win = QtWidgets.QApplication(argv), QtWidgets.QMainWindow()
    ui = UI(win, bk)
    app.exec_()
    return ui.para


def getstr(qtext):
    try:
        return qtext.text().strip()
    except:
        return ''


class UI(Ui_panel):
    def __init__(self, panel, bk):
        sdir, self.bk = path.join(bk._w.plugin_dir, bk._w.plugin_name), bk
        self.config, self.para = path.join(sdir, 'config.json'), None
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        self.setupUi(panel)
        panel.setWindowIcon(QtGui.QIcon.fromTheme(
            path.join(sdir, 'plugin.png')))
        self.auto_check.toggled['bool'].connect(
            lambda x: panel.setFixedSize(500, 310 if x else 150))
        self.load_config()
        self.auto_check.toggled.connect(self.check_input)
        self.t2s_check.toggled.connect(self.check_input)
        self.cps_check.toggled.connect(self.check_input)
        self.sub_check.toggled.connect(self.check_input)
        self.flow_class.toggled.connect(self.check_input)
        self.flow_tag.toggled.connect(self.check_input)
        self.flow_text.toggled.connect(self.check_input)
        self.flow_title.toggled.connect(self.check_input)
        self.flow_note.toggled.connect(self.check_input)
        self.flow_image.toggled.connect(self.check_input)
        self.flow_page.toggled.connect(self.check_input)
        self.isbn.textChanged.connect(lambda: self.isbn.setText(
            chkisbn.sub('', self.isbn.text())[:13]))
        self.title.textChanged.connect(self.check_input)
        self.subtitle.textChanged.connect(self.check_input)
        self.volume.textChanged.connect(self.check_input)
        self.isbn.textChanged.connect(self.check_input)
        self.writer.textChanged.connect(self.check_input)
        self.painter.textChanged.connect(self.check_input)
        self.translator.textChanged.connect(self.check_input)
        self.introducer.textChanged.connect(self.check_input)
        self.inputer.textChanged.connect(self.check_input)
        self.epuber.textChanged.connect(self.check_input)
        self.summary.textChanged.connect(self.check_input)
        self.launch_start.clicked.connect(self.submit)
        self.config_reset.clicked.connect(self.reset_config)
        self.to_content.clicked.connect(lambda: startfile(sdir))
        self.to_github.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(
            QtCore.QUrl('https://github.com/Minami926494/STERA')))
        self.from_opf.clicked.connect(self.get_opfinfo)
        panel.show()

    def load_config(self):
        if path.exists(self.config):
            with open(self.config) as config:
                para = loads(config.read())
            self.auto_check.setChecked(para['auto']), self.t2s_check.setChecked(para['t2s']), self.sub_check.setChecked(para['sub']),  self.cps_check.setChecked(para['cps']),  self.chk_check.setChecked(para['chk']), self.tem_check.setChecked(para['tem']), self.del_check.setChecked(para['del']), self.flow_class.setChecked(para['flow_class']), self.flow_tag.setChecked(para['flow_tag']), self.flow_text.setChecked(para['flow_text']), self.flow_title.setChecked(para['flow_title']), self.flow_note.setChecked(para['flow_note']), self.flow_image.setChecked(
                para['flow_image']), self.flow_page.setChecked(para['flow_page']), self.title.setText(para['tit']), self.volume.setText(para['vol']), self.subtitle.setText(para['stit']), self.isbn.setText(para['isbn']), self.writer.setText(para['writer']), self.painter.setText(para['painter']), self.translator.setText(para['translator']), self.introducer.setText(para['introducer']), self.inputer.setText(para['inputer']), self.epuber.setText(para['epuber']), self.summary.setPlainText(setsum.sub('', para['summary']))

    def reset_config(self):
        if path.exists(self.config):
            remove(self.config)
        self.auto_check.setChecked(True), self.t2s_check.setChecked(True), self.sub_check.setChecked(True),  self.cps_check.setChecked(True),  self.chk_check.setChecked(True), self.tem_check.setChecked(True), self.del_check.setChecked(True), self.flow_class.setChecked(True), self.flow_tag.setChecked(True), self.flow_text.setChecked(True), self.flow_title.setChecked(True), self.flow_note.setChecked(
            True), self.flow_image.setChecked(True), self.flow_page.setChecked(True), self.title.setText(''), self.volume.setText(''), self.subtitle.setText(''), self.isbn.setText(''), self.writer.setText(''), self.painter.setText(''), self.translator.setText(''), self.introducer.setText(''), self.inputer.setText(''), self.epuber.setText(''), self.summary.setPlainText('')

    def check_input(self):
        self.launch_start.setEnabled((len(getstr(self.title)) and len(getstr(self.isbn)) and len(getstr(self.writer)) and len(getstr(self.painter)) and len(getstr(self.translator)) and len(getstr(self.introducer)) and len(getstr(self.inputer)) and len(getstr(self.epuber))) and (self.flow_class.isChecked() or self.flow_tag.isChecked(
        ) or self.flow_text.isChecked() or self.flow_title.isChecked() or self.flow_note.isChecked() or self.flow_image.isChecked() or self.flow_page.isChecked())) if self.auto_check.isChecked() else self.launch_start.setEnabled(self.t2s_check.isChecked() or self.cps_check.isChecked() or self.sub_check.isChecked())

    def get_opfinfo(self):
        meta = f2p.sub(lambda x: chr(ord(x.group(0))-65248),
                       self.bk.getmetadataxml())
        tit, isbn = gettit.search(meta), getisbn.search(meta)
        if tit:
            title = tit.group(1)
            sub, vol = getsub.search(title), getvol.search(title)
            if sub:
                title = title.replace(sub.group(0), '')
                self.subtitle.setText(sub.group(1))
            else:
                self.subtitle.setText('')
            if vol:
                title = title.replace(vol.group(0), '')
                self.volume.setText(vol.group(2).zfill(2))
            else:
                self.volume.setText('')
            self.title.setText(title.strip())
        self.isbn.setText(isbn.group(1) if isbn else '')

    def submit(self):
        self.para = {'auto': self.auto_check.isChecked(), 't2s': self.t2s_check.isChecked(), 'sub': self.sub_check.isChecked(), 'cps': self.cps_check.isChecked(), 'chk': self.chk_check.isChecked(), 'tem': self.tem_check.isChecked(), 'del': self.del_check.isChecked(), 'flow_class': self.flow_class.isChecked(), 'flow_tag': self.flow_tag.isChecked(), 'flow_text': self.flow_text.isChecked(), 'flow_title': self.flow_title.isChecked(), 'flow_note': self.flow_note.isChecked(
        ), 'flow_image': self.flow_image.isChecked(), 'flow_page': self.flow_page.isChecked(), 'tit': getstr(self.title), 'vol': getstr(self.volume), 'stit': getstr(self.subtitle), 'isbn': getstr(self.isbn), 'writer': getstr(self.writer), 'painter': getstr(self.painter), 'translator': getstr(self.translator), 'introducer': getstr(self.introducer), 'inputer': getstr(self.inputer), 'epuber': getstr(self.epuber), 'summary': getsum.sub('', self.summary.toHtml()) if self.summary.toPlainText() else ''}
        with open(self.config, mode='w') as config:
            config.write(dumps(self.para))
        QtCore.QCoreApplication.quit()
