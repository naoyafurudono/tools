#!/usr/bin/env python3
# アーティスト/アルバム/タイトル.mp3に分類・変換する

import multiprocessing
from os import path
import os
from typing import Tuple
import sys

#sys.path.append(path.join(path.dirname(__file__), "lib~"))
import ffmpeg


def run(
    target_dir: str,
    target_extension: str,
    obj_extension: str,
    out_dir: str,
    quiet: bool,
):
    table = {}
    for target_path in (
        path.join(target_dir, filename)
        for filename in os.listdir(target_dir)
        if filename.endswith(target_extension)
    ):
        info = ffmpeg.probe(target_path)["format"]["tags"]
        title = info["title"]
        album = info["album"]
        artist = info["artist"]
        dir_path = path.join(artist, album)
        obj_path = path.join(out_dir, dir_path, title + obj_extension)

        table[target_path] = obj_path

    for obj_path in set(table.values()):
        os.makedirs(os.path.dirname(obj_path), exist_ok=True)
    with multiprocessing.Pool() as p:
        p.map(conv, ((frm, to, quiet) for (frm, to) in table.items()))


def conv(args: Tuple[str, str, bool]):
    frm, to, quiet = args
    ffmpeg.input(frm).output(to).run(quiet=quiet)


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
        target_extension=args.target_extension,
        obj_extension=args.object_extension,
        out_dir=args.out,
        quiet=args.quiet,
    )


def file_extension(name: str) -> str:
    if len(name) <= 1 or name[0] != ".":
        raise ValueError()
    return name


if __name__ == "__main__":
    main()
