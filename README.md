# Python Learning Examples

Python 初心者向けのサンプルプログラム集です。

じゃんけん、クイズ、数独ソルバー、シューティングゲームなど、基本的な文法や処理の流れを学ぶための小さなプログラムをまとめています。

## サンプル一覧

| フォルダ | 内容 |
| --- | --- |
| `janken` | コンソールで遊ぶじゃんけんゲーム |
| `quiz` | JSON ファイルから問題を読み込むクイズゲーム |
| `sudoku` | 数独を解くサンプルプログラム |
| `shooting_game` | `pygame-ce` を使った簡単なシューティングゲーム |

## 必要な環境

- Python 3.14 以降
- pip

このリポジトリでは、Python 3.14 に対応しやすいように `pygame` ではなく `pygame-ce` を使用しています。

## セットアップ

リポジトリを取得し、フォルダに移動します。

```powershell
git clone <repository-url>
cd python-learning-examples
```

仮想環境を作成して有効化します。

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

必要なライブラリをインストールします。

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 実行方法

### じゃんけん

```powershell
cd janken
python janken.py
```

### クイズ

```powershell
cd quiz
python quiz_sample.py
```

クイズの問題は `quiz/quiz.json` に定義されています。
問題を追加する場合は、JSON 配列の中に次の形式のデータを追加します。

```json
{
  "Difficulty": 1,
  "Genre": ["Python"],
  "Qestion": "Pythonで文字を表示するときに使う関数はどれですか？",
  "Choices": [
    "print",
    "input",
    "range"
  ],
  "Answer": 0
}
```

各項目の意味は次の通りです。

| 項目 | 内容 |
| --- | --- |
| `Difficulty` | 難易度です。0 から 5 の範囲で指定します。 |
| `Genre` | ジャンルです。複数指定できるようにリストで書きます。 |
| `Qestion` | 問題文です。現在のプログラムではこのキー名を使っています。 |
| `Choices` | 選択肢です。リストで指定します。 |
| `Answer` | 正解の選択肢番号です。先頭を `0` として数えます。 |

`Answer` は画面に表示される番号ではなく、`Choices` のリスト番号で指定します。
たとえば、1 番目の選択肢が正解なら `0`、2 番目なら `1`、3 番目なら `2` です。

JSON では、最後の要素の後ろにカンマを付けないように注意してください。

### 数独ソルバー

コンソールで解く場合は、次のコマンドを実行します。

```powershell
cd sudoku
python sudoku_solver.py
```

ブラウザ画面で数値を入力して解く場合は、次のコマンドでWebアプリを起動します。

```powershell
cd sudoku
python app.py
```

起動後、ブラウザで次のURLを開きます。

```text
http://127.0.0.1:5000
```

画面のマスに分かっている数字を入力し、`解く` ボタンを押すと答えが表示されます。
空欄のマスはそのままで構いません。

### シューティングゲーム

```powershell
cd shooting_game
python sample_game.py
```

シューティングゲームは画像ファイルを `img` フォルダから読み込むため、必ず `shooting_game` フォルダに移動してから実行してください。

## 依存ライブラリ

依存ライブラリは [requirements.txt](requirements.txt) にまとめています。

```txt
numpy
pygame-ce
Flask
```

## 学習ポイント

- 変数、条件分岐、繰り返し
- 関数の作成と呼び出し
- リスト、辞書、タプルの使い方
- JSON ファイルの読み込み
- 再帰処理
- Flask を使った簡単なWebアプリ
- `pygame-ce` を使った画像表示、キー入力、ゲームループ

## 補足

`pygame-ce` は `pygame` と同じように、コード内では基本的に `import pygame` と書いて使用できます。
