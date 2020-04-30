import os
from tkinter import filedialog, Tk
import platform
import re
"""
なんだっけこれ？？？

ファイル名から不要部分をはぎ取っているっぽい。
汎用性は低い
"""

def select_file():
    # Windowsの場合withdrawの状態だとダイアログも
    # 非表示になるため、rootウィンドウを表示する
    if system == "Windows":
        root.deiconify()
    # macOS用にダイアログ作成前後でupdate()を呼ぶ
    root.update()
    # ダイアログを前面に
    root.lift()
    root.focus_force()
    path_str = filedialog.askdirectory()
    root.update()
    if system == "Windows":
        # 再度非表示化（Windowsのみ）
        root.withdraw()
    return path_str




if __name__ == "__main__":
    # ダイアログ用のルートウィンドウの作成
    root = Tk()
    # ウィンドウサイズを0にする（Windows用の設定）
    root.geometry("0x0")
    # ウィンドウのタイトルバーを消す（Windows用の設定）
    root.overrideredirect(1)
    # ウィンドウを非表示に
    root.withdraw()
    system = platform.system()

    root_path = select_file()
    dirlist = os.listdir(root_path)
    dirlist = [root_path + os.sep + dr for dr in dirlist]

    pattern = "r\[*\]"

    for dr in dirlist:
        res = re.match(pattern, os.path.basename(dr))
        if os.path.isdir(dr):
            if dr.endswith(" [High-Resolution]"):
                os.rename(dr, dr.rstrip(" [High-Resolution]"))
            if res is not None:
                print(dr)
                os.rename(dr, root_path + os.sep + os.path.basename(dr).lstrip(res.group()))