# アーティスト/アルバム/タイトル.mp3に分類・変換する

from multiprocessing import Pool
import os
from typing import Callable, Tuple
import ffmpeg

THREAD = 12


def is_target(file_path: str) -> bool:
    return file_path.endswith(".3gp")


def run(
    target_dir: str,
    out_dir: str = "out",
    is_target_filepath: Callable[[str], bool] = is_target,
    obj_extension: str = ".mp3",
):
    filenames = map(lambda name: os.path.join(target_dir, name), os.listdir(target_dir))
    table = {}
    for filepath in filter(is_target_filepath, filenames):
        info = ffmpeg.probe(filepath)["format"]["tags"]
        title = info["title"]
        album = info["album"]
        artist = info["artist"]
        dirpath = os.path.join(artist, album)
        obj_path = os.path.join(out_dir, dirpath, title + obj_extension)
        table[filepath] = obj_path

    for frm, to in table.items():
        os.makedirs(os.path.dirname(to), exist_ok=True)
    with Pool(THREAD) as p:
        p.map(conv, table.items())


def conv(inst: Tuple[str, str]):
    frm, to = inst
    ffmpeg.input(frm).output(to).run()


if __name__ == "__main__":
    run(target_dir='Unknown Album')
