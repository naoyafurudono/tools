# structure music files

- 楽曲ファイルのメタデータをもとにアーティスト、アルバムごとにフォルダに振り分ける。
- 並行してフォーマットも変更する。
- フォーマット変更は並列実行するのでそれなりに早い。
- `ffmpeg`のラッパー。

## 使い方

### 前準備

1. `ffmpeg`のインストール
    - 各自頑張ること
1. 依存ライブラリのインストール
    - `poetry install`

### コマンドの使用

```
peotry run python main.py <args>
```

```
usage: main.py [-h] [-o OUT] [--object-extension OBJECT_EXTENSION] -t TARGET_EXTENSION target_dir

positional arguments:
  target_dir

options:
  -h, --help            show this help message and exit
  -o OUT, --out OUT     output directly name
  --object-extension OBJECT_EXTENSION
                        result file extension
  -t TARGET_EXTENSION, --target-extension TARGET_EXTENSION
                        input file extension used to filter files
```

## 例

カレントディレクトリに以下のような`hectopascal`フォルダがあるとする。

```
hectopascal
├── 01 hectopascal.m4a
├── 02 好き、以外の言葉で.m4a
├── 03 hectopascal (instrumental).m4a
├── 04 好き、以外の言葉で (instrumental).m4a
├── AlbumArtSmall.jpg
└── Folder.jpg
```

以下を実行する。

```sh
./main.py -t ".m4a" hectopascal/
```

カレントディレクトリに以下のように`out`フォルダが作られる。

```
out
└── 小糸侑 (高田憂希) & 七海燈子 (寿美菜子)
   └── hectopascal
      ├── hectopascal (instrumental).mp3
      ├── hectopascal.mp3
      ├── 好き、以外の言葉で (instrumental).mp3
      └── 好き、以外の言葉で.mp3
```

アーティストやアルバム名がファイルごとに異なる場合は、適切にフォルダを作成してファイルを分類する。
