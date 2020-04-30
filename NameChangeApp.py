# -*- coding:utf-8 -*-
"""
ディレクトリを選択後、選択ディレクトリ内の音楽ファイルのファイル名をタグ情報をもとに変換
"""

import os
import platform
from pathlib import Path
from tkinter import filedialog, Tk

from mutagen.aiff import AIFF
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC


class NameChangeApp:

    def __init__(self):

        self.system = platform.system()
        self.root = Tk()
        self.root.geometry("0x0")
        self.root.overrideredirect(1)
        self.root.withdraw()
        self.directory = self.select_dir()
        self.filelist = self.make_filelist()

    def make_filelist(self):
        root_path = Path(self.directory)
        pathlist = root_path.glob("**/*")
        pathlist = [str(p) for p in pathlist if os.path.isfile(p)]

        return pathlist

    def name_change(self):

        for path in self.filelist:
            os.chdir(os.path.dirname(path))
            file = os.path.basename(path)

            # tagsにタグのディクショナリを読み込む
            if file.endswith("flac"):
                try:
                    tags = FLAC(file)
                    name = ','.join(tags['title'])
                    end = ".flac"
                except:
                    print("タグエラー: " + path)
                    continue
            elif file.endswith("mp3"):
                try:
                    tags = EasyID3(file)
                    name = ','.join(tags['title'])
                    end = ".mp3"
                except:
                    print("タグエラー: " + path)
                    continue
            elif file.endswith("aiff") or file.endswith("aif"):
                try:
                    tags = AIFF(file)
                    name = ','.join(tags['TIT2'].text)
                    end = ".aif"
                except:
                    print("タグエラー: " + path)
                    continue
            else:
                continue
                # {'TIT2': TIT2(encoding=<Encoding.UTF16: 1>, text=['幻惑SILHOUETTE']),
                # 'TALB': TALB(encoding=<Encoding.UTF16: 1>, text=['THE IDOLM@STER SHINY COLORS BRILLI@NT WING 03 バベルシティ・グレイス']),
                # 'TCOP': TCOP(encoding=<Encoding.UTF16: 1>, text=['(P)Lantis']),
                # 'TSOT': TSOT(encoding=<Encoding.UTF16: 1>, text=['ゲンワクSILHOUETTE']),
                # 'TSOA': TSOA(encoding=<Encoding.UTF16: 1>, text=['IDOLM@STER SHINY COLORS BRILLI@NT WING 03 バベルシティ・グレイス']),
                # 'TCON': TCON(encoding=<Encoding.UTF16: 1>, text=['ゲーム']),
                # 'TRCK': TRCK(encoding=<Encoding.LATIN1: 0>, text=['2/3']),
                # 'TPOS': TPOS(encoding=<Encoding.LATIN1: 0>, text=['1/1']),
                # 'TPE1': TPE1(encoding=<Encoding.UTF16: 1>, text=['アンティーカ']),
                # 'TPE2': TPE2(encoding=<Encoding.UTF16: 1>, text=['アンティーカ']),
                # 'TCOM': TCOM(encoding=<Encoding.UTF16: 1>, text=['no_my']),
                # 'COMM::eng': COMM(encoding=<Encoding.UTF16: 1>, lang='eng', desc=''...

            # ここから拡張子の対応を増やせる

            # replace()で禁止文字を削除
            original = name.replace("\"", " ").replace("\\", " ").replace("/", " ").replace("*", " ").replace(":",
                                                                                                              " ").replace(
                "|", " ").replace("<", " ").replace(">", " ").replace("?", " ")
            name = original + end

            i = 1
            if name != file:
                while os.path.exists(name):
                    i += 1
                    name = original + " " + str(i) + end

            os.rename(path, os.getcwd() + os.sep + name)

    def select_dir(self):
        if self.system == "Windows":
            self.root.deiconify()
            # macOS用にダイアログ作成前後でupdate()を呼ぶ
        self.root.update()
        # ダイアログを前面に
        self.root.lift()
        self.root.focus_force()
        path_str = filedialog.askdirectory()
        self.root.update()
        if self.system == "Windows":
            # 再度非表示化（Windowsのみ）
            self.root.withdraw()
        return path_str


if __name__ == "__main__":
    while True:
        # print("ok")
        nca = NameChangeApp()
        if nca.directory == "":
            break

        nca.name_change()
