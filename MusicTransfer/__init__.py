import os
import shutil
import tkinter as tk
import tkinter.filedialog as filedialog
from pathlib import Path

from mutagen import aiff, easyid3, flac

import config
from concurrent import futures


def make_dist_path(tag):
    if isinstance(tag, aiff.AIFF):
        try:
            artist = ','.join(tag["TPE1"].text).replace("/", "･")
            album = ','.join(tag["TALB"].text).replace("/", "･")
            return Path(artist + os.sep + album)
        except:
            print("必要なタグ情報がたりません")
            return None
    else:
        try:
            artist = ','.join(tag["artist"]).replace("/", "･")
            album = ','.join(tag["album"]).replace("/", "･")
            return Path(artist + os.sep + album)
        except:
            print("必要なタグ情報がたりません")
            return None


def tag_scanner(music_path):
    if music_path.suffix == ".aiff" or music_path.suffix == ".aif":
        return aiff.AIFF(music_path)
    elif music_path.suffix == ".flac":
        return flac.FLAC(music_path)
    elif music_path.suffix == ".mp3":
        return easyid3.EasyID3(music_path)
    else:
        print("Invalid FileType")


class MusicTransfer:
    def __init__(self):
        self.cf = config.Config()
        self.new_music = filedialog.askopenfilenames()
        self.new_music = list(map(Path, self.new_music))
        self.new_music_tags = [tag_scanner(music) for music in self.new_music]
        # self.dist_path = [make_dist_path(tag) for tag in self.new_music_tags]
        self.dist_path = []

    def move_files(self):
        for music, path in zip(self.new_music, self.dist_path):

            player_dist = self.cf.player_main_path.joinpath(path)
            if not player_dist.exists():
                os.makedirs(player_dist)

            backup_dist = self.cf.backup_path.joinpath(path)
            if not backup_dist.exists():
                os.makedirs(backup_dist)

            with futures.ThreadPoolExecutor(max_workers=4) as e:
                e.submit(shutil.copy2, music, player_dist)
                e.submit(shutil.copy2, music, backup_dist)

    def btn_clicked(self):
        for i, e in enumerate(entries):
            if e.get() != "":
                self.dist_path.append(Path(e.get()))
            else:
                self.dist_path.append(make_dist_path(self.new_music_tags[i]))

        self.move_files()


def main():
    mt = MusicTransfer()
    # mt.move_files()

    root = tk.Tk()
    root.title("Music Transfer")

    frame1 = tk.Frame(root)
    frame2 = tk.Frame(root)
    frame1.pack()
    frame2.pack()

    labels = []
    header1 = tk.Label(frame1, text="曲名")
    header2 = tk.Label(frame1, text="出力先")

    header1.grid(row=0, column=0)
    header2.grid(row=0, column=1)

    for nm in mt.new_music:
        labels.append(tk.Label(frame1, text=nm.stem))
    for i, label in enumerate(labels):
        label.grid(row=i + 1, column=0)

    global entries
    entries = []
    for i in range(len(labels)):
        entries.append(tk.Entry(frame1))
    for i, entry in enumerate(entries):
        entry.grid(row=i + 1, column=1)

    button = tk.Button(frame2, text="実行", command=mt.btn_clicked)
    button.pack(anchor="e")

    root.mainloop()


if __name__ == "__main__":
    main()
