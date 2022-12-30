#!/usr/bin/env python3
# アーティスト/アルバム/タイトル.mp3に分類・変換する

from multiprocessing import Pool
import os
from typing import Callable, Tuple
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "lib~"))
import ffmpeg

THREAD = 12


def run(
    target_dir: str,
    out_dir: str,
    obj_extension: str,
    is_target_filename: Callable[[str], bool],
    quiet: bool,
):
    table = {}
    for target_path in (
        os.path.join(target_dir, filename)
        for filename in os.listdir(target_dir)
        if is_target_filename(filename)
    ):
        info = ffmpeg.probe(target_path)["format"]["tags"]
        title = info["title"]
        album = info["album"]
        artist = info["artist"]
        dir_path = os.path.join(artist, album)
        obj_path = os.path.join(out_dir, dir_path, title + obj_extension)
        table[target_path] = obj_path

    for obj_path in table.values():
        os.makedirs(os.path.dirname(obj_path), exist_ok=True)
    with Pool(THREAD) as p:
        p.map(conv, table.items())


def conv(inst: Tuple[str, str]):
    frm, to = inst
    ffmpeg.input(frm).output(to).run(quiet=quit)


def main():
    import argparse

    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("target_dir")
    parser.add_argument(
        "-t",
        "--target-extension",
        required=True,
        help="input file extension used to filter files",
        type=file_extension,
    )
    parser.add_argument(
        "--object-extension",
        required=False,
        default=".mp3",
        help="result file extension",
        type=file_extension,
    )
    parser.add_argument(
        "-o",
        "--out",
        required=False,
        default="out",
        help="output directly name",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        required=False,
        default=True,
        action="store_true",
    )
    args = parser.parse_args()

    run(
        target_dir=args.target_dir,
        out_dir=args.out,
        obj_extension=args.object_extension,
        is_target_filename=lambda filepath: filepath.endswith(args.target_extension),
        quiet=args.quiet,
    )


def file_extension(name: str) -> str:
    if len(name) <= 1 or name[0] != ".":
        raise ValueError()
    return name


if __name__ == "__main__":
    main()
