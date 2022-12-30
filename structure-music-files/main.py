# アーティスト/アルバム/タイトル.mp3に分類・変換する

import argparse
from multiprocessing import Pool
import os
from typing import Callable, Tuple
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "lib~"))
import ffmpeg

THREAD = 12


def is_target(file_path: str) -> bool:
    return file_path.endswith(".3gp")


def run(
    target_dir: str,
    out_dir: str,
    obj_extension: str,
    is_target_filepath: Callable[[str], bool] = is_target,
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
    parser = argparse.ArgumentParser("python3 main.py")
    parser.add_argument("target_dir")
    parser.add_argument(
        "-o", "--out", required=False, default="out", help="output directly name"
    )
    parser.add_argument(
        "--object_extension",
        required=False,
        default=".mp3",
        help="result file extension",
    )
    parser.add_argument(
        "-t",
        "--target_extension",
        required=True,
        default=".3gp",
        help="input file extension used to filter files",
    )
    args = parser.parse_args()
    run(
        target_dir=args.target_dir,
        out_dir=args.out,
        obj_extension=args.object_extension,
        is_target_filepath=lambda filepath: filepath.endswith(args.target_extension),
    )
