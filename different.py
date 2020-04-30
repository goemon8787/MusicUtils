# coding:utf-8
"""
arg1: パス1
arg2: パス2

パス2にあってパス1にないファイルのリストを表示
"""


import os
from pathlib import Path
import shutil
from tkinter import Tk, filedialog


# パス2にあってパス1にないものを表示
def file_check(path1, path2):
    p1 = Path(path1)
    p2 = Path(path2)

    pathset1 = set(p1.glob("**/*"))
    pathset2 = set(p2.glob("**/*"))

    nameset1 = set(os.path.basename(str(f)) for f in pathset1)
    nameset2 = set(os.path.basename(str(f)) for f in pathset2)

    nameset3 = nameset2 - nameset1

    pathset3 = [str(path) for path in pathset2 if os.path.basename(str(path)) in nameset3]

    return pathset3


if __name__ == "__main__":
    distpath = filedialog.askdirectory()
    path1 = filedialog.askdirectory()
    path2 = filedialog.askdirectory()

    filelist = file_check(path1, path2)

    for f in filelist:
        try:
            shutil.move(f, distpath)
        except:
            print("移動エラー: ", f)
